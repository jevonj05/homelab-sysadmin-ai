from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv

from agent.checks.disk_check import get_disk_usage
from agent.checks.docker_check import get_docker_health
from agent.checks.network_check import check_network
from agent.checks.system_check import get_system_health
from agent.ollama_client import analyze_snapshot


def collect_snapshot(path: str) -> dict[str, Any]:
    return {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "disk": get_disk_usage(path),
        "system": get_system_health(),
        "network": check_network(),
        "docker": get_docker_health(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Local-first homelab diagnostic assistant")
    parser.add_argument("--path", default="/", help="Filesystem path to inspect")
    parser.add_argument("--no-ai", action="store_true", help="Collect telemetry without Ollama analysis")
    parser.add_argument("--json", action="store_true", help="Print telemetry as JSON")
    args = parser.parse_args()

    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    snapshot = collect_snapshot(args.path)

    if args.json or args.no_ai:
        print(json.dumps(snapshot, indent=2))
    if args.no_ai:
        return 0

    try:
        analysis = analyze_snapshot(snapshot)
        if not args.json:
            print(json.dumps(snapshot, indent=2))
        print("\nAI ANALYSIS\n-----------")
        print(analysis or "Ollama returned an empty response.")
    except Exception as exc:
        logging.error("AI analysis unavailable: %s", exc)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
