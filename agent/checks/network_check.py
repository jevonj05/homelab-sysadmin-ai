from __future__ import annotations

import socket
import time
from typing import Any


def check_network(host: str = "1.1.1.1", port: int = 53, timeout: float = 2.0) -> dict[str, Any]:
    """Test outbound TCP reachability without invoking a shell."""
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency = round((time.perf_counter() - started) * 1000, 1)
            return {"target": f"{host}:{port}", "reachable": True,
                    "latency_ms": latency, "status": "healthy"}
    except OSError as exc:
        return {"target": f"{host}:{port}", "reachable": False,
                "status": "warning", "error": str(exc)}
