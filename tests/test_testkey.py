from testkey import load_env


def test_all_set(monkeypatch):
    # Arrange
    monkeypatch.setenv("KIMI", "A_VAL")
    monkeypatch.setenv("DSEEK", "B_VAL")
    monkeypatch.setenv("OPENAI", "C_VAL")

    # Act
    result = load_env()

    # Assert
    assert result == {"KIMI": "A_VAL", "DSEEK": "B_VAL", "OPENAI": "C_VAL"}


def test_missing(monkeypatch):
    # Ensure env vars are not set
    monkeypatch.delenv("KIMI", raising=False)
    monkeypatch.delenv("DSEEK", raising=False)
    monkeypatch.delenv("OPENAI", raising=False)

    # Act
    result = load_env()

    # Assert
    assert result == {
        "KIMI": "<KIMI not set>",
        "DSEEK": "<DSEEK not set>",
        "OPENAI": "<OPENAI not set>",
    }
