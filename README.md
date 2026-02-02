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

### Run tests

```bash
# from project root (with the virtualenv activated)
python -m pytest -q
```

---

## 🔐 Environment variables
This project reads the following environment variables in `testkey.load_env()`:
- `KIMI`
- `DSEEK`
- `OPENAI`

If a variable is missing, `load_env()` returns a default placeholder (e.g. `<KIMI not set>`).

---

If you want, I can add a GitHub Actions workflow to run tests on push. 👍
