# testkey.py - test file for project testKey

import os
import sys
from typing import Dict

from .snake import run_snake_game


def load_env() -> Dict[str, str]:
    """Return the environment variables of interest with sensible defaults."""
    return {
        "KIMI": os.environ.get("KIMI", "<KIMI not set>"),
        "DSEEK": os.environ.get("DSEEK", "<DSEEK not set>"),
        "OPENAI": os.environ.get("OPENAI", "<OPENAI not set>"),
    }


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "snake":
        run_snake_game()
        return
    print("Hello from testkey in project testKey")
    print("Run `testkey snake` to play Snake.")
    # Do not print environment-sensitive values by default.


if __name__ == "__main__":
    main()
