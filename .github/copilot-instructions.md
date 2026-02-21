# testkey Project - AI Agent Instructions

## Project Overview
This is a dual-purpose Python project:
1. **Core testkey library** ([src/testkey.py](../src/testkey.py)): Demonstrates environment variable loading with sensible defaults for `KIMI`, `DSEEK`, and `OPENAI` keys
2. **FileViewer application** ([FileViewer/](../FileViewer/)): Standalone GUI application with both Tkinter and PyQt6 implementations for directory browsing

The core library has **zero runtime dependencies** and is deliberately minimal. FileViewer is an independent subproject with its own GUI dependencies.

## Project Structure
- **src/testkey.py** - Core library: `load_env()` returns dict with env vars or placeholder defaults like `<KIMI not set>`
- **tests/** - pytest tests using `monkeypatch` for env var isolation
- **FileViewer/** - Independent GUI app (not part of testkey package)
  - `fileviewer.py` - Tkinter implementation
  - `fileviewer_pyqt6.py` - PyQt6 implementation  
  - `launcher.py` - UI launcher to choose between implementations
  - Has its own `.venv/` virtualenv separate from root project

## Development Workflow

### Environment Setup
```bash
# Use virtualenv at .venv (standard for this project)
python3 -m venv .venv
source .venv/bin/activate

# Install from pinned dev-requirements.txt (preferred)
python -m pip install -r dev-requirements.txt
```

### Running Tests
```bash
# From project root with virtualenv activated
python -m pytest -q
```

Tests follow Arrange-Act-Assert pattern with pytest's `monkeypatch` for environment isolation. See [tests/test_testkey.py](../tests/test_testkey.py) for examples.

### CI/CD
GitHub Actions ([.github/workflows/ci.yml](../workflows/ci.yml)) runs tests on Python 3.10, 3.11, 3.13 using `dev-requirements.txt`.

## Key Conventions

### Environment Variable Handling
- `load_env()` always returns a dict, never raises exceptions for missing vars
- Default placeholders follow pattern: `<VARNAME not set>`
- Never print sensitive env values in production code

### Testing Patterns
- Use `monkeypatch.setenv()` to set variables in tests
- Use `monkeypatch.delenv(raising=False)` to ensure vars are unset
- Follow Arrange-Act-Assert structure with comments

### Dependencies
- **Runtime**: None (intentionally zero dependencies for core library)
- **Dev**: Pinned versions in `dev-requirements.txt` (currently pytest==9.0.2)
- When adding dependencies, update both `dev-requirements.txt` and `pyproject.toml [project.optional-dependencies]`

## FileViewer Notes
- Separate from main testkey package - not imported or tested with main project
- Has dual implementations (Tkinter/PyQt6) selectable via launcher
- Maintains its own virtualenv at `FileViewer/.venv/`

## Release Process
Release notes go in `releases/MAJOR.MINOR.PATCH.md` with date, summary, changes, verification steps, and future notes. See [releases/0.1.0.md](../releases/0.1.0.md).
