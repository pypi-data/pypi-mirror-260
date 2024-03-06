# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import base64
import io
import json
import os
import re
import sys
import tempfile
import time
import typing as t
from collections import deque, Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cached_property
from math import floor
from threading import Lock
from uuid import UUID

import psutil
import pytermor as pt
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw
from es7s_commons import AdaptiveFragment, DisposableComposite, CompositeCompressor

from es7s.cmd._base import _BaseAction
from es7s.shared import (
    get_logger,
    get_stdout,
    SMALLEST_PIXEL_7,
    ShutdownableThread,
    with_terminal_state,
    ProxiedTerminalState,
    ShutdownInProgress,
    boolsplit,
    sub,
    get_stderr,
    is_x11,
    run_subprocess,
)
from es7s.shared.fusion_brain import FusionBrainAPI
from es7s.shared.path import get_font_file
from es7s.shared.uconfig import get_merged, get_for


class action(_BaseAction):
    def __init__(
        self,
        threads: int,
        prompt: list[str],
        stdin: bool,
        style: str,
        **kwargs,
    ):
        self._threads = threads
        if threads < 1:
            # threads_limit = self.uconfig().get("auto-threads-limit", int)
            self._threads = max(1, psutil.cpu_count())
        if stdin:
            prompt = sys.stdin.read()
        else:
            prompt = " ".join(prompt)
        prompt = prompt.strip()
        if not prompt:
            get_stderr().echo("Empty input")
            return

        auth_cfg = get_merged().get_section("auth")
        self._api = FusionBrainAPI(
            auth_cfg.get("fusion-brain-api-key"),
            auth_cfg.get("fusion-brain-secret"),
        )
        if not self._auth():
            return
        style_names = self._api.fetch_styles()
        get_logger().info("Supported styles: " + ", ".join(style_names))
        if style not in style_names:
            get_logger().warning(f"Unsupported style '{style}'")  # , falling back to '{style_fb}'")

        self._queue = Queue(self._api, self._threads, prompt, style, **kwargs)
        self._run()

    def _auth(self) -> bool:
        try:
            return bool(self._api.fetch_model())
        except Exception as e:
            raise RuntimeError("Auth failed, unable to proceed") from e

    @with_terminal_state(no_cursor=True)
    def _run(self, termstate: ProxiedTerminalState):
        try:
            sys.stdout.flush()
            self._queue.run()
        finally:
            self._queue.destroy()


class Queue:
    _THREAD_POLL_TIME_SEC = 0.1

    start_ts: float = None

    @staticmethod
    def now() -> float:
        return time.time_ns()

    def __init__(
        self,
        api: FusionBrainAPI,
        threads: int,
        prompt_raw: str,
        style: str,
        width: int,
        height: int,
        times: int,
        no_retry: bool,
        no_open: bool,
        delete: bool,
        **kwargs,
    ):
        self.tasks = deque[Task]()
        self.tasks_done = deque[Task]()
        self.tasks_lock = Lock()

        self.style = style
        self.keep_origins = not delete
        self._open_merged = not no_open

        self._workers = deque[Worker](maxlen=threads)
        self._exceptions = deque[tuple["Worker", t.Optional["Task"], Exception]]()
        self.merged_paths: list[str] = []

        super().__init__()

        prompt_lines: list[str] = [*pt.filtere(line.strip() for line in prompt_raw.splitlines())]
        tasks_total = times * len(prompt_lines)
        for r_idx in range(times):
            for (p_idx, p) in enumerate(prompt_lines):
                task_idx = len(self.tasks)
                pre_start_delay_s = task_idx / 2 if task_idx < threads else 0
                task = Task(p, p_idx, task_idx, tasks_total, pre_start_delay_s, (width, height))
                self.tasks.append(task)

        for w_idx in range(min(len(self.tasks), threads)):
            self._workers.append(Worker(w_idx, no_retry, self, api.copy()))

        self.pp = ProgressPrinter()
        self.im = ImageMerger(prompt_lines, width)

    def run(self):
        Queue.start_ts = Queue.now()

        for worker in self._workers:
            worker.start()

        while self._workers:
            worker: Worker = self._workers[0]
            worker.join(self._THREAD_POLL_TIME_SEC)

            if worker.is_alive():
                # self.pp.update(worker.task)  # avoid complete freezing on network delays
                self._workers.rotate()
            else:
                self._workers.remove(worker)

    def get_next_task(self) -> t.Optional["Task"]:
        if not self.tasks:
            return None
        if self.tasks_lock.acquire(timeout=1):
            task = self.tasks.popleft()
            task.task_start_ts = self.now() + task.pre_start_delay_s * 1e9
            self.tasks_lock.release()
            return task
        return None

    def set_task_completed(self, task: "Task"):
        task.is_finished = True
        self.tasks_done.append(task)

    def defer_exception(self, worker: "Worker", task: t.Optional["Task"], e: Exception):
        self._exceptions.append((worker, task, e))

    def destroy(self):
        self.merged_paths = self.im.merge_all(self.keep_origins, self.style)
        self.pp.close()

        self.pp.print_exceptions(self._exceptions)

        results = []
        for task in self.tasks_done:
            results.extend(task.statuses)
        results_by_type = Counter(results)
        avg_job_durations_ns = [*pt.filtern(t.avg_job_duration for t in self.tasks_done)]
        avg_job_duration_s = 0
        if avg_job_durations_ns:
            avg_job_duration_s = (sum(avg_job_durations_ns) / len(avg_job_durations_ns)) / 1e9
        self.pp.print_summary(results_by_type, avg_job_duration_s)

        for merged_path in self.merged_paths:
            get_stdout().echo(merged_path)
        if is_x11() and self._open_merged and self.merged_paths:
            run_subprocess("xdg-open", self.merged_paths[0])


class Status(str, pt.ExtendedEnum):
    QUEUED = "queued"

    PENDING = "pending"
    REFUSED = "refused"
    RECEIVED = "received"
    ERROR = "error"

    CANCEL = "cancel"
    FAILURE = "failure"
    SUCCESS = "success"


@dataclass(frozen=True)
class StatusStyle:
    char: pt.RT
    name: pt.FT
    duration: pt.FT

    @cached_property
    def msg(self) -> pt.FT:
        if self.name:
            return pt.FrozenStyle(self.name, bold=True)
        return pt.NOOP_STYLE


class StatusStyles(dict):
    def __init__(self):
        C_IP = "□"
        C_DONE = "■"
        ST_OK = pt.make_style(pt.cv.GREEN)
        ST_NOK = pt.make_style(pt.cv.RED)
        ST_WARN = pt.make_style(pt.cv.YELLOW)
        ST_STALE = pt.make_style(pt.cv.GRAY_50)
        ST_TIME = pt.make_style(pt.cv.BLUE)

        super().__init__(
            {
                Status.PENDING: self._make(C_IP, pt.NOOP_STYLE, ST_TIME),
                Status.QUEUED: self._make("", ST_STALE),
                Status.REFUSED: self._make(C_DONE, ST_WARN),
                Status.RECEIVED: self._make(C_IP, ST_OK),
                Status.ERROR: self._make(C_IP, ST_NOK),
                Status.CANCEL: self._make(C_IP, ST_NOK),
                Status.FAILURE: self._make(C_DONE, ST_NOK),
                Status.SUCCESS: self._make(C_DONE, ST_OK),
            }
        )

    def _make(self, char: str, st_char_name: pt.FT, st_time: pt.FT = None) -> StatusStyle:
        return StatusStyle(
            pt.Fragment(char, st_char_name) if st_char_name else char,
            st_char_name,
            st_time or st_char_name,
        )


_styles = StatusStyles()


@dataclass()
class Task:
    MIN_FETCH_INTERVAL_SEC = 4

    prompt: str
    prompt_idx: int
    task_idx: int
    tasks_total: int
    pre_start_delay_s: float = 0.0
    size: tuple[int, int] = (1024, 1024)

    max_width: int = pt.get_terminal_width()

    job_uuid: UUID | None = None
    images: list[str] = field(default_factory=list)
    statuses: list[Status] = field(default_factory=list)
    task_start_ts: float | None = None
    job_start_ts: float | None = None
    last_fetch_ts: float | None = None
    task_duration_ns: float | None = None
    job_durations_ns: list[float] = field(default_factory=list)
    jobs_done: int = 0
    msg: str | tuple[str, str] | None = None
    is_finished: bool = False

    @cached_property
    def state_printer(self) -> "TaskStatePrinter":
        return TaskStatePrinter(self)

    @property
    def current_status(self) -> Status:
        if not self.statuses:
            return Status.QUEUED
        return self.statuses[-1]

    @property
    def avg_job_duration(self) -> float | None:
        if self.jobs_done:
            return sum(self.job_durations_ns) / self.jobs_done
        return None

    def assign_job_uuid(self, uuid: UUID):
        self.job_uuid = uuid
        self.job_start_ts = Queue.now()
        self.last_fetch_ts = None

    def is_allowed_to_generate(self) -> bool:
        return Queue.now() >= self.task_start_ts

    def is_allowed_to_fetch(self) -> bool:
        if self.last_fetch_ts is None:
            return True
        return (Queue.now() - self.last_fetch_ts) / 1e9 >= self.MIN_FETCH_INTERVAL_SEC

    def set_status(self, rr: Status, msg: str | tuple[str, str] = None):
        self.statuses.append(rr)
        self.msg = msg
        self.last_fetch_ts = Queue.now()
        self.task_duration_ns = Queue.now() - self.task_start_ts

    def append_images(self, images: list[str]):
        self.images += images
        self.set_status(Status.RECEIVED)
        self.job_durations_ns.append(Queue.now() - self.job_start_ts)
        self.job_start_ts = None
        self.jobs_done += 1


class Worker(ShutdownableThread):
    _POLL_TIME_SEC = 0.15
    DEFAULT_GENERATION_ATTEMPTS = 5

    def __init__(
        self,
        worker_idx: int,
        no_retry: bool,
        queue: Queue,
        api: FusionBrainAPI,
    ):
        self.worker_idx = worker_idx
        self._no_retry = no_retry
        self._queue = queue
        self._api = api

        self.task: Task | None = None

        super().__init__("fudra", thread_name=f"worker:{self.worker_idx}")

    def _reset(self):
        self.task = None

    def run(self):
        while True:
            if self.is_shutting_down():
                self.destroy()
                return

            if not self.task:
                self.task = self._queue.get_next_task()
                if not self.task:
                    self.shutdown()
                    continue

            if self.task:
                try:
                    self._generate()
                    self._write_image()
                except ShutdownInProgress:
                    pass
                except Exception as e:
                    self._queue.defer_exception(self, self.task, e)
                    self.task.set_status(Status.FAILURE, repr(e))
                finally:
                    self._queue.set_task_completed(self.task)
                    self._redraw()
                    self._reset()

    def _update(self):
        self._queue.pp.update(self.task)

    def _redraw(self):
        self._queue.pp.redraw(self.task)

    def _tick(self):
        if self.is_shutting_down():
            self.task.set_status(Status.CANCEL)
            raise ShutdownInProgress
        time.sleep(self._POLL_TIME_SEC)
        self._update()

    def _generate(self):
        gen_attempts = 1 if self._no_retry else self.DEFAULT_GENERATION_ATTEMPTS
        while gen_attempts > 0 and len(self.task.images) == 0:
            if not self.task.is_allowed_to_generate():
                self._tick()
                continue

            gen_attempts -= 1
            negprompt, posprompt = boolsplit(
                self.task.prompt.split(), lambda p: bool(re.match(r"^-[^-]", p))
            )
            generation_uuid = self._api.generate(
                " ".join(posprompt),
                [np.removeprefix("-") for np in negprompt],
                self._queue.style,
                self.task.size,
            )
            self.task.assign_job_uuid(generation_uuid)
            self._update()

            fetch_attempts = 30
            while fetch_attempts > 0:
                self._tick()

                if self.task.is_allowed_to_fetch():
                    fetch_attempts -= 1
                    images, censored, resp = self._api.check_generation(self.task.job_uuid)

                    if not resp.ok:
                        self.task.set_status(Status.ERROR, f"HTTP {resp.status_code}")
                        e = RuntimeError(f"Request failed with HTTP {resp.status_code}")
                        self._queue.defer_exception(self, self.task, e)
                    elif censored:
                        self.task.set_status(Status.REFUSED, str(self.task.job_uuid))
                    elif len(images) > 0:
                        self.task.append_images(images)
                    else:
                        self.task.set_status(Status.PENDING)

                    self._update()
                    if self.task.current_status != Status.PENDING:
                        break

            self._update()

    def _write_image(self):
        if not self.task.images:
            return

        output_dir = os.path.expanduser(get_for(self).get("output-dir", str, fallback="~"))
        os.makedirs(output_dir, exist_ok=True)

        basename = f"fb-{Queue.start_ts / 1e9:.0f}"
        origin_basename = f"{basename}-{self.task.prompt_idx}-{self.task.task_idx}"
        merged_basename = f"{basename}-{self.task.prompt_idx}-merged"

        with open(os.path.join(output_dir, f"{origin_basename}.json"), "wt") as f:
            json.dump(dict(prompt=self.task.prompt), f)

        for idx, img_b64 in enumerate(self.task.images):
            img_in = io.BytesIO(img_b64.encode("utf8"))
            img_out = io.BytesIO()
            base64.decode(img_in, img_out)

            last_img_path = os.path.join(output_dir, f"{origin_basename}-{idx}.jpg")
            self._write_image_origin(img_out, last_img_path)

            last_img_info = (
                os.path.basename(last_img_path),
                pt.format_bytes_human(os.stat(last_img_path).st_size).rjust(5),
            )
            self.task.set_status(Status.SUCCESS, last_img_info)
            self._queue.im.add_image(self.task.prompt_idx, f"{merged_basename}.jpg", last_img_path)

    def _write_image_origin(self, img: io.BytesIO, target_path: str):
        img.seek(0)
        with open(target_path, "wb") as f:
            f.write(img.read())


class ImageMerger:
    def __init__(self, prompt_lines: list[str], img_width: int):
        self._prompt_lines = prompt_lines
        self._img_width = img_width

        self._pidx_to_imgs_map: dict[int, list[str]] = {}
        self._pidx_to_filename_map: dict[int, str] = {}

        self._labeler = ImageLabeler()

    def add_image(self, prompt_idx: int, merged_filename: str, img_path: str):
        if prompt_idx not in self._pidx_to_imgs_map.keys():
            self._pidx_to_imgs_map.update({prompt_idx: []})
        self._pidx_to_imgs_map.get(prompt_idx).append(img_path)
        self._pidx_to_filename_map.update({prompt_idx: merged_filename})

    def merge_all(self, keep_origins: bool, style: str) -> list[str]:
        output_paths = []
        for prompt_idx, img_paths in self._pidx_to_imgs_map.items():
            out_filename = os.path.abspath(self._pidx_to_filename_map[prompt_idx])
            label_filename = self._labeler.make_label_image(
                self._prompt_lines[prompt_idx], self._img_width, style
            )
            args = [
                *img_paths,
                # ("fx_montage", "5,,0,0,0,6,0,0,0,255,0,0,0,0,0"),  # with borders, but causes resampling
                ("fx_montage", "5,,0,0,0,0,0,0,0,255,0,0,0,0,0"),
                label_filename,
                ("append", "y"),
                ("normalize", "1,255"),
                ("o", out_filename),
            ]
            sub.run_subprocess("gmic", *pt.flatten(args), executable="gmic")
            # os.unlink(label_filename)

            output_paths.append(out_filename)
            if not keep_origins:
                get_logger().info("Removing the origins")
                for img in img_paths:
                    os.unlink(img)
            else:
                get_logger().info("Keeping the origins")
        return output_paths


class ImageLabeler:
    LABEL_FONT = ImageFont.truetype(str(get_font_file(SMALLEST_PIXEL_7)), 10)

    def make_label_image(self, prompt: str, width: int, style: str) -> str:
        prompt_split = []

        im = Image.new("RGBA", (width, 256))
        while prompt:
            tlen = Draw(im).textlength(prompt, self.LABEL_FONT)
            overflow_ratio = tlen / im.width
            edge = len(prompt) / overflow_ratio
            if overflow_ratio < 1:
                prompt_split.append(prompt)
                prompt = ""
            else:
                edge = floor(edge)
                try:
                    nearest_space = prompt.rindex(" ", 0, edge)
                    prompt_split.append(prompt[:nearest_space])
                    prompt = prompt[nearest_space + 1 :]
                except ValueError:
                    prompt_split.append(prompt[:edge])
                    prompt = prompt[edge:]

        prompt_joined = f"[{style}] " + "\n".join(prompt_split)
        kwargs = dict(
            xy=(6, 6),
            text=prompt_joined,
            font=self.LABEL_FONT,
            stroke_width=1,
            spacing=0,
        )
        box = Draw(im).multiline_textbbox(**kwargs)
        imtx = Image.new("RGBA", box[2:], (255, 255, 255, 0))
        Draw(imtx).multiline_text(
            **kwargs,
            fill=(255, 255, 255, 255),
            stroke_fill=(0, 0, 0, 255),
        )
        im.paste(imtx, None, imtx)
        imtx.close()
        im = im.crop((0, 0, box[2] + box[0], box[3] + box[1]))

        fid, fname = tempfile.mkstemp(suffix=".png")
        with open(fname, "wb") as f:
            im.save(f)
            im.close()
        return fname


class ProgressPrinter:
    _ts_last_termw_query: float = None
    _max_width: int = None

    def __init__(self):
        self._redraw_lock = Lock()
        self._cursor_line = 0
        self._task_lines: deque[Task | None] = deque()

    def update(self, task: Task):
        if not task:
            return
        with self._redraw_lock:
            if task not in self._task_lines:
                self._go_to_bottom()
                self._task_lines.append(task)
            else:
                task_line = self._task_lines.index(task)
                self._go_to(task_line)
            self._draw(task)

    def redraw(self, task: Task):
        self.update(task)
        with self._redraw_lock:
            self._task_lines[self._task_lines.index(task)] = None

    def _draw(self, task: Task, suffix: str = ""):
        get_stderr().echoi_rendered("\n")
        get_stderr().echoi_rendered(task.state_printer.print_state() + suffix)
        get_stderr().echoi(pt.make_move_cursor_up())

    def _go_to(self, target_line: int):
        delta = abs(self._cursor_line - target_line)
        if self._cursor_line > target_line:
            get_stderr().echoi(pt.make_move_cursor_up(delta))
        elif self._cursor_line < target_line:
            get_stderr().echoi(pt.make_move_cursor_down(delta))
        get_stderr().echoi(pt.make_set_cursor_column())
        self._cursor_line = target_line

    def _go_to_bottom(self):
        self._go_to(len(self._task_lines))

    def _clear_line(self):
        get_stderr().echoi(pt.make_clear_line())

    def close(self):
        self._go_to_bottom()
        get_stderr().echo("")

    def print_exceptions(self, exceptions: t.Sequence[tuple[Worker, Task | None, Exception]]):
        if not exceptions:
            return
        get_stderr().echo(f"There was {len(exceptions)} error(s):")

        for (_, task, e) in exceptions:
            msg = pt.Text()
            if task:
                msg += pt.Fragment(pt.pad(2) + f"Task #{task.task_idx+1}", pt.Styles.ERROR_LABEL)
            msg += pt.Fragment(pt.pad(2) + repr(e), pt.Styles.ERROR)
            get_stderr().echo_rendered(msg)

    def print_summary(self, results_by_type: Counter[Status], avg_job_duration_s: float):
        refused = results_by_type.get(Status.REFUSED) or 0
        recevied = results_by_type.get(Status.RECEIVED) or 0
        requested = refused + recevied
        if requested > 0:
            refusal_ratio = 100 * refused / requested
        else:
            refusal_ratio = 0

        st_refcnt = pt.Style(fg=pt.cv.YELLOW)
        if refused == 0:
            st_refcnt.fg = pt.cv.GRAY_50
        st_refrat = pt.Style(st_refcnt, bold=True)

        sep = "-" * 40
        get_stderr().echo("\n" + sep)

        print_summary_line = lambda t, *f: get_stderr().echo_rendered(
            pt.Text(pt.fit(t, 12, ">") + ":", pt.pad(1), *f)
        )
        print_summary_line(
            "Refusal rate",
            (f"{refusal_ratio:3.1f}%", st_refrat),
            f" ({pt.Fragment(str(refused), st_refcnt)}/{requested})",
        )
        print_summary_line(
            "Avg.job time",
            pt.format_time_delta(avg_job_duration_s),
        )
        get_stderr().echo(sep)

    @classmethod
    def get_max_width(cls) -> int:
        if not cls._max_width or (time.time() - cls._ts_last_termw_query >= 1):
            cls._max_width = pt.get_terminal_width()
            cls._ts_last_termw_query = time.time()
        return cls._max_width


class TaskStatePrinter:
    def __init__(self, task: Task):
        self._task = task

    def print_state(self) -> pt.RT:
        task = self._task

        sts = _styles.get(task.current_status)
        st0 = pt.NOOP_STYLE
        stm = lambda c: st0.clone().merge_overwrite(pt.make_style(c))
        stmf = lambda c: st0.clone().merge_fallback(pt.make_style(c))
        if task.is_finished:
            st0 = stm(pt.Style(fg=pt.cv.GRAY_50))
        sep = lambda: (DisposableComposite(pt.pad(1)), pt.pad(1))

        cols = []
        cols.append(AdaptiveFragment(5, f"{task.task_idx + 1:>02d}/{task.tasks_total:<02d} ", st0))
        cols.extend(sep())
        cols.append(AdaptiveFragment(8, task.prompt, st0))
        cols.extend(sep())

        if not task.msg:
            cols.append(AdaptiveFragment(6, str(task.job_uuid or "").ljust(36), st0))
        else:
            cols.append(AdaptiveFragment(6, self._print_msg(task.msg, 36, 1), stm(sts.msg)))
        cols.extend(sep())

        col_dur = pt.fit("---", 8, ">")
        if task.task_start_ts and task.current_status != Status.QUEUED:
            task_start_delta = Queue.now() - task.task_start_ts
            if task_start_delta > 0:
                col_dur = pt.format_time_delta(task_start_delta / 1e9).rjust(8)
        cols.append(AdaptiveFragment(8, col_dur, stmf(sts.duration)))
        cols.extend(sep())

        cols.append(AdaptiveFragment(4, task.current_status.value.rjust(9), stm(sts.name)))
        cols.extend(sep())

        cols.extend(self._print_status_history(task.statuses, st0))

        result = CompositeCompressor(*cols)
        result.compress(ProgressPrinter.get_max_width())
        return result

    def _print_msg(self, msg: str | tuple[str, str], maxlen: int = 30, gap: int = 2) -> str:
        if isinstance(msg, tuple):
            return pt.fit(msg[0], maxlen - len(msg[1]) - gap, "<") + pt.pad(gap) + msg[1]
        return pt.fit(msg, maxlen, "<", keep="<")

    def _print_status_history(
        self, statuses: list[Status], base_st: pt.Style
    ) -> Iterable[pt.Fragment]:
        for status in statuses:
            char = _styles.get(status).char
            if isinstance(char, str):
                yield pt.Fragment(char, base_st)
            else:
                yield char
