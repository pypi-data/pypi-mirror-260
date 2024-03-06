import atexit
import logging
import os
import re
import subprocess
from typing import Any, List

import requests
import simplejson
from django.conf import settings
from django.http import HttpRequest
from django.utils.html import escape

renderer_process_addrs: dict[int, str] = {}
logger = logging.getLogger("django.server")


def wait_and_get_addr() -> str:
    if renderer := os.environ.get("REACTIVATED_RENDERER", None):
        return renderer

    # Store the server address in a mapping key'ed by this processes PID. This
    # way, if/when this process forks, the new process will still start its own
    # SSR server.
    pid = os.getpid()
    if pid in renderer_process_addrs:
        return renderer_process_addrs[pid]

    renderer_process = subprocess.Popen(
        [
            "node",
            f"{settings.BASE_DIR}/node_modules/_reactivated/renderer.js",
        ],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        cwd=settings.BASE_DIR,
        env={**os.environ.copy(), "NODE_ENV": "production"},
    )
    atexit.register(lambda: renderer_process.terminate())

    output = ""

    for c in iter(lambda: renderer_process.stdout.read(1), b""):  # type: ignore[union-attr]
        output += c

        if matches := re.findall(r"RENDERER:(.*?):LISTENING", output):
            renderer_process_addrs[pid] = matches[0].strip()
            return renderer_process_addrs[pid]
    assert False, "Could not bind to renderer"


def get_accept_list(request: HttpRequest) -> List[str]:
    """
    Given the incoming request, return a tokenized list of media
    type strings.

    From https://github.com/encode/django-rest-framework/blob/master/rest_framework/negotiation.py
    """
    header = request.META.get("HTTP_ACCEPT", "*/*")
    return [token.strip() for token in header.split(",")]


def should_respond_with_json(request: HttpRequest) -> bool:
    accepts = get_accept_list(request)

    return request.GET.get("format", None) == "json" or any(
        ["application/json" in content_type for content_type in accepts]
    )


session = requests.Session()


def render_jsx_to_string(request: HttpRequest, context: Any, props: Any) -> str:
    respond_with_json = should_respond_with_json(request)

    payload = {"context": context, "props": props}
    data = simplejson.dumps(payload)
    headers = {"Content-Type": "application/json"}

    if "debug" in request.GET:
        return f"<html><body><h1>Debug response</h1><pre>{escape(data)}</pre></body></html>"
    elif (
        respond_with_json
        or "raw" in request.GET
        or getattr(settings, "REACTIVATED_SERVER", False) is None
    ):
        request._is_reactivated_response = True  # type: ignore[attr-defined]
        return data

    address = wait_and_get_addr()
    response = session.post(f"{address}/_reactivated/", headers=headers, data=data)

    if response.status_code == 200:
        return response.text  # type: ignore[no-any-return]
    else:
        try:
            error = response.json()
        except requests.JSONDecodeError:  # type: ignore[attr-defined]
            raise Exception(response.content)
        else:
            raise Exception(error["stack"])
