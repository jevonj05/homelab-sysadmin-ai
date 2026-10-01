from __future__ import annotations

import subprocess
from typing import Any

# Commands are selected by application-owned action IDs. LLM/user text is never
# interpolated into shell commands.
ALLOWED_ACTIONS: dict[str, list[str]] = {
    "disk_free": ["df", "-h"],
    "memory": ["free", "-h"],
    "docker_ps": ["docker", "ps", "--all"],
    "ip_addresses": ["ip", "-brief", "address"],
}


def available_actions() -> list[str]:
    return sorted(ALLOWED_ACTIONS)


def run_action(action: str, timeout: int = 10) -> dict[str, Any]:
    command = ALLOWED_ACTIONS.get(action)
    if command is None:
        return {"status": "denied", "action": action, "error": "action_not_allowlisted"}

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            shell=False,
        )
        return {
            "status": "ok" if completed.returncode == 0 else "error",
            "action": action,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "error", "action": action, "error": str(exc)}
