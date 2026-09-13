"""LLM sağlayıcı soyutlaması. Tek interface: LLMClient.complete(messages) -> str."""
from __future__ import annotations

import random
import time
from abc import ABC, abstractmethod

import requests


class LLMError(Exception):
    """Yeniden denemelerle de aşılamayan hata."""


class LLMClient(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> str:
        """messages: [{"role": ..., "content": ...}, ...] -> asistanın ham metin çıktısı."""
        raise NotImplementedError


class OpenAICompatClient(LLMClient):
    """OpenAI-uyumlu /chat/completions konuşan somut istemci.

    Sağlayıcıya özel hiçbir şey yok: base_url + api_key + model config'den gelir.
    429 / 5xx / bağlantı hatası -> exponential backoff (Retry-After başlığına uyar).
    """

    RETRY_STATUSES = {408, 409, 425, 429}

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        *,
        temperature: float = 0.7,
        max_tokens: int | None = 1024,
        timeout: float = 90.0,
        max_retries: int = 8,
        base_delay: float = 2.0,
        max_delay: float = 60.0,
        extra_headers: dict | None = None,
        extra_body: dict | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.extra_headers = dict(extra_headers or {})
        self.extra_body = dict(extra_body or {})
        self._session = requests.Session()

    # --- yardımcılar ---------------------------------------------------------
    def _retryable(self, status: int) -> bool:
        return status in self.RETRY_STATUSES or 500 <= status < 600

    @staticmethod
    def _retry_after(resp: requests.Response) -> float | None:
        ra = resp.headers.get("Retry-After")
        if not ra:
            return None
        try:
            return max(0.0, float(ra))
        except ValueError:
            return None

    @staticmethod
    def _extract(data: dict) -> str:
        choices = data.get("choices") or []
        if not choices:
            raise LLMError(f"yanıtta 'choices' yok: {str(data)[:300]}")
        msg = choices[0].get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):  # bazı sağlayıcılar parça listesi döndürür
            content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
        return content or ""

    # --- ana çağrı -----------------------------------------------------------
    def complete(self, messages: list[dict]) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            **self.extra_headers,
        }
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            **self.extra_body,
        }
        if self.max_tokens:
            body["max_tokens"] = self.max_tokens

        delay = self.base_delay
        last_err = "?"
        for attempt in range(self.max_retries + 1):
            retry_after = None
            try:
                resp = self._session.post(url, json=body, headers=headers, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout) as e:
                last_err = f"bağlantı hatası: {e}"
            else:
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                    except ValueError:
                        last_err = f"JSON değil: {resp.text[:200]}"
                    else:
                        err = data.get("error") if isinstance(data, dict) else None
                        if err:  # bazı sağlayıcılar hatayı 200 gövdesinde döndürür
                            code = err.get("code") if isinstance(err, dict) else None
                            if isinstance(code, int) and self._retryable(code):
                                last_err = f"gövde hatası {code}: {str(err)[:200]}"
                            else:
                                raise LLMError(f"sağlayıcı hatası: {str(err)[:500]}")
                        else:
                            return self._extract(data)
                elif self._retryable(resp.status_code):
                    last_err = f"HTTP {resp.status_code}: {resp.text[:200]}"
                    retry_after = self._retry_after(resp)
                else:
                    raise LLMError(f"HTTP {resp.status_code}: {resp.text[:500]}")

            if attempt == self.max_retries:
                break
            wait = retry_after if retry_after is not None else delay
            wait = min(wait, self.max_delay) + random.uniform(0, 0.5)
            time.sleep(wait)
            delay = min(delay * 2, self.max_delay)

        raise LLMError(f"{self.max_retries} yeniden denemeden sonra başarısız: {last_err}")
