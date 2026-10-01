# Security Model

## Trust boundaries

System telemetry, container names, image tags, logs, and future external data are untrusted. They may contain text that resembles instructions.

## LLM isolation

Telemetry is serialized and placed between explicit data delimiters. The system prompt tells the model to treat that content only as data. This reduces, but does not eliminate, prompt-injection risk.

## Command execution

The model is not given arbitrary command execution. `command_runner.py` maps fixed action identifiers to fixed argument arrays and uses `subprocess.run(..., shell=False)`. No LLM-produced string is interpolated into a shell command.

## Privilege

The project is designed to run without root for normal diagnostics. Do not run the application as root merely to increase collector coverage.

## Secrets

Runtime settings belong in `.env`, which is ignored by Git. Do not place API keys, credentials, tokens, private IP inventories, or sensitive logs in the repository.

## Future hardening

- Per-action authorization and confirmation
- Structured LLM output validation
- Persistent append-only audit records
- Collector data minimization/redaction
- Unit tests for adversarial telemetry
