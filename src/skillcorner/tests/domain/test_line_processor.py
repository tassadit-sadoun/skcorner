import json

from skillcorner.application.line_processor import DefaultLineProcessor


def process(line, n):
    return DefaultLineProcessor().process(line, n)


# ==========================================================
# 1. PRIORITY CORE (most important rule)
# ==========================================================


def test_multiple_of_5_overrides_all():
    assert process("$ hello world.", 10) == "Multiple of 5"

    line = json.dumps({"a": 1})
    assert process(line, 10) == "Multiple of 5"


# ==========================================================
# 2. DOLLAR RULE
# ==========================================================


def test_dollar_rule():
    assert process("hello $ world", 1) == "hello_$_world"


# ==========================================================
# 3. DOT RULE
# ==========================================================


def test_dot_rule():
    assert process("hello world.", 1) == "hello world."


# ==========================================================
# 4. JSON RULE (happy + edge)
# ==========================================================


def test_json_rule():
    line = json.dumps({"a": 1})
    result = process(line, 2)

    parsed = json.loads(result)

    assert parsed["a"] == 1
    assert "even" in parsed


def test_invalid_json():
    assert process("{invalid json", 2) == "Nothing to display"


# ==========================================================
# 5. FALLBACK
# ==========================================================


def test_fallback():
    assert process("hello", 1) == "Nothing to display"
