from __future__ import annotations

from plan_and_act.utils.llm import _redact_secrets


def test_redact_secrets_masks_openai_key_patterns() -> None:
    text = "token sk-proj-abc123_DEF and sk-legacy-xyz789 should be redacted"
    redacted = _redact_secrets(text)

    assert "sk-proj-abc123_DEF" not in redacted
    assert "sk-legacy-xyz789" not in redacted
    assert redacted.count("[REDACTED_OPENAI_KEY]") == 2
