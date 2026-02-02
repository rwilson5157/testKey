# testkey.py - test file for project testKey

import os
from typing import Dict


def load_env() -> Dict[str, str]:
    """Return the environment variables of interest with sensible defaults."""
    return {
        "KIMI": os.environ.get("KIMI", "<KIMI not set>"),
        "DSEEK": os.environ.get("DSEEK", "<DSEEK not set>"),
        "OPENAI": os.environ.get("OPENAI", "<OPENAI not set>"),
    }


def main():
    print("Hello from t.stkey.py in project testKey")
    # Do not print environment-sensitive values by default.


if __name__ == "__main__":
    main()
