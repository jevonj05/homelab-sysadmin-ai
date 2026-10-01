# Setup

## Requirements

- Linux
- Python 3.10+
- Docker (optional collector)
- Ollama (optional AI analysis)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Pull or select your local Ollama model separately, then set `OLLAMA_MODEL` in `.env`.

## Usage

```bash
python -m agent.main --path /mnt/storage
python -m agent.main --path /mnt/storage --no-ai
python -m agent.main --path / --no-ai --json
pytest -q
```

Docker health depends on the current user having legitimate access to the Docker daemon.
