# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t

import bs4
import requests

from es7s.shared import requester, get_stdout
from ._base import _BaseAction


class action_complement(_BaseAction):
    def __init__(self, **kwargs):
        self._requester = requester.Requester()
        self._run(**kwargs)

    def _run(self, word: t.Iterable[str], raw: bool):
        stdout = get_stdout()

        url = f"https://sinonim.org/kb/{' '.join(word)}"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        resp = self._requester.make_request(
            url, request_fn=lambda: requests.get(url, headers=headers)
        )

        try:
            html = bs4.BeautifulSoup(resp.text, features="lxml")
        except:
            html = None

        if raw or not html:
            stdout.echo(html.prettify() if html else resp.text)
            return

        for result in html.find(id="assocPodryad").find_all(class_="riLi"):
            stdout.echo(result.text)
