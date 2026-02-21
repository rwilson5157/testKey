# testkey 🧪

[![CI](https://github.com/rwilson5157/testKey/actions/workflows/ci.yml/badge.svg)](https://github.com/rwilson5157/testKey/actions)

Small test project that demonstrates loading environment variables and running tests.

---

## 🚀 Quickstart (dev)

### Prerequisites
- Python 3.8+ (this project uses a virtualenv at `.venv` when configured)

### Install dev dependencies
Option A — using the pinned `dev-requirements.txt` (recommended):

```bash
# create and activate a virtualenv (if you don't already have one)
python3 -m venv .venv
source .venv/bin/activate

# install dev deps
python -m pip install --upgrade pip
python -m pip install -r dev-requirements.txt
```

Option B — using `pyproject.toml` optional dependencies (if you prefer):

```bash
# Install editable package and extras (may require a modern pip)
python -m pip install -e '.[dev]'
```

Note: `-e '.[dev]'` installs this project in editable mode plus the `dev` extras (currently `pytest`).
In offline or restricted network environments, you may need to create the venv with
`python -m venv --system-site-packages .venv` so build tooling like `setuptools` is available locally.

### Run tests

```bash
# from project root (with the virtualenv activated)
python -m pytest -q
```

### Run Snake

```bash
# from project root (with the virtualenv activated)
python -m testkey snake
```

Controls:
- Arrow keys or `W/A/S/D` to move
- `P` to pause/resume
- `R` to restart after game over (or anytime)
- `Q` to quit

Manual verification checklist:
- Controls move exactly one grid cell per tick and reverse direction is blocked.
- Eating food increases score by 1 and grows snake length by 1.
- Hitting walls or self ends the game and freezes movement.
- `P` toggles pause/resume without changing score or position while paused.
- `R` restarts to a fresh game state with score reset to 0.

---

## 🔐 Environment variables
This project reads the following environment variables in `testkey.load_env()`:
- `KIMI`
- `DSEEK`
- `OPENAI`

If a variable is missing, `load_env()` returns a default placeholder (e.g. `<KIMI not set>`).
