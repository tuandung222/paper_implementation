from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import BadRequestError, OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


class LLMClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.base_url = os.getenv("OPENAI_BASE_URL", "").strip()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def _build_client(self) -> OpenAI:
        kwargs: dict[str, Any] = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return OpenAI(**kwargs)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=6))
    def chat_json(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
    ) -> dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("OPENAI_API_KEY is not set")

        client = self._build_client()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=messages,
            )
            content = response.choices[0].message.content or "{}"
            return _parse_json_content(content)
        except BadRequestError as exc:
            if "response_format" not in str(exc):
                raise

        # Fallback for models/endpoints that don't support response_format=json_object.
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=messages,
        )
        content = response.choices[0].message.content or "{}"
        return _parse_json_content(content)


def _parse_json_content(content: str) -> dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", content, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return json.loads(fenced.group(1))

    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(content[start : end + 1])

    raise ValueError(f"Model output is not valid JSON: {content}")
