from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any


class ComfyUIError(RuntimeError):
    pass


class ComfyUIClient:
    """Small stdlib-only client for a local ComfyUI API server."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _json(self, path: str, payload: dict[str, Any] | None = None) -> Any:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {} if body is None else {"Content-Type": "application/json"}
        request = urllib.request.Request(self.base_url + path, data=body, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ComfyUIError(f"ComfyUI {path} returned HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ComfyUIError(f"ComfyUI request failed for {path}: {exc}") from exc

    def system_stats(self) -> dict[str, Any]:
        return self._json("/system_stats")

    def queue(self) -> dict[str, Any]:
        return self._json("/queue")

    def node_types(self) -> set[str]:
        info = self._json("/object_info")
        if not isinstance(info, dict):
            raise ComfyUIError("ComfyUI /object_info returned an unexpected response")
        return set(info)

    def submit(self, workflow: dict[str, Any], client_id: str) -> str:
        queue = self.queue()
        running = queue.get("queue_running", [])
        pending = queue.get("queue_pending", [])
        if running or pending:
            raise ComfyUIError(
                f"Refusing to start while ComfyUI queue is occupied: "
                f"{len(running)} running, {len(pending)} pending"
            )
        result = self._json("/prompt", {"prompt": workflow, "client_id": client_id})
        if not isinstance(result, dict) or not result.get("prompt_id"):
            raise ComfyUIError(f"ComfyUI rejected the workflow: {result}")
        return str(result["prompt_id"])

    def wait(self, prompt_id: str, timeout_s: float = 1800.0, poll_s: float = 2.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            history = self._json(f"/history/{prompt_id}")
            entry = history.get(prompt_id) if isinstance(history, dict) else None
            if isinstance(entry, dict):
                status = entry.get("status", {})
                status_name = str(status.get("status_str", "")).lower()
                if status.get("completed") is True or status_name in {"success", "error"}:
                    if status_name == "error" or status.get("completed") is False:
                        raise ComfyUIError(f"ComfyUI job failed: {json.dumps(entry, ensure_ascii=False)}")
                    return entry
            time.sleep(poll_s)
        raise ComfyUIError(f"Timed out waiting for ComfyUI prompt {prompt_id}")
