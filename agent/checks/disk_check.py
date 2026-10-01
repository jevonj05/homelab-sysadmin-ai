from __future__ import annotations

import shutil
from typing import Any


def get_disk_usage(path: str) -> dict[str, Any]:
    """Return disk capacity and a simple health classification for path."""
    try:
        total, used, free = shutil.disk_usage(path)
    except FileNotFoundError:
        return {"path": path, "status": "error", "error": "path_not_found",
                "message": f"Disk path not found: {path}"}
    except PermissionError:
        return {"path": path, "status": "error", "error": "permission_denied",
                "message": f"Permission denied: {path}"}
    except OSError as exc:
        return {"path": path, "status": "error", "error": "os_error",
                "message": str(exc)}

    gb = 1024 ** 3
    percent = round((used / total) * 100, 2) if total else 0.0
    status = "healthy" if percent < 80 else "warning" if percent < 90 else "critical"
    return {
        "path": path,
        "total_gb": round(total / gb, 2),
        "used_gb": round(used / gb, 2),
        "free_gb": round(free / gb, 2),
        "used_percentage": percent,
        "status": status,
    }
