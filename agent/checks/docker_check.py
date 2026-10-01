from __future__ import annotations

from typing import Any

try:
    import docker
except ImportError:
    docker = None


def get_docker_health() -> dict[str, Any]:
    """Summarize local Docker container state."""
    if docker is None:
        return {"status": "unavailable", "error": "docker_sdk_not_installed", "containers": []}
    try:
        client = docker.from_env()
        client.ping()
        containers = client.containers.list(all=True)
        items = [{"name": c.name, "status": c.status, "image": ", ".join(c.image.tags) or c.image.short_id}
                 for c in containers]
        stopped = sum(1 for item in items if item["status"] != "running")
        return {
            "status": "healthy" if stopped == 0 else "warning",
            "container_count": len(items),
            "non_running_count": stopped,
            "containers": items,
        }
    except Exception as exc:
        return {"status": "unavailable", "error": "docker_unreachable",
                "message": str(exc), "containers": []}
