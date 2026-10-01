from __future__ import annotations

import platform
import time
from typing import Any

import psutil


def get_system_health() -> dict[str, Any]:
    """Collect basic host health without requiring elevated privileges."""
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.2)
    boot = psutil.boot_time()
    status = "critical" if cpu >= 95 or memory.percent >= 95 else (
        "warning" if cpu >= 85 or memory.percent >= 85 else "healthy"
    )
    return {
        "hostname": platform.node(),
        "platform": platform.system(),
        "kernel": platform.release(),
        "cpu_percentage": cpu,
        "memory_percentage": memory.percent,
        "memory_available_gb": round(memory.available / (1024 ** 3), 2),
        "uptime_hours": round((time.time() - boot) / 3600, 1),
        "status": status,
    }
