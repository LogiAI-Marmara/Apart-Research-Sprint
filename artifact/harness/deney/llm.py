"""LLM sağlayıcı soyutlaması. Tek interface: LLMClient.complete(messages) -> Yanit."""
from __future__ import annotations

import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests


class LLMError(Exception):
    """Yeniden denemelerle de aşılamayan hata."""


@dataclass
class Yanit:
    """Tek tamamlama sonucu.

    metin         asistanın ham metin çıktısı (content). Muhakeme alanları (reasoning_content /
                  reasoning) buraya ASLA konmaz: muhakeme aksiyon değildir.
    finish_reason choices[0].finish_reason (ör. "stop", "length"); sağlayıcı vermediyse None.
    bos_icerik    content boş/None geldi (muhakeme dolu olsa bile). Çağıran bunu KESILDI sayar.
    """

    metin: str
    finish_reason: str | None = None
    bos_icerik: bool = False


class LLMClient(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> Yanit:
        """messages: [{"role": ..., "content": ...}, ...] -> Yanit (metin + finish_reason + bos_icerik)."""
        raise NotImplementedError


class OpenAICompatClient(LLMClient):
    """OpenAI-uyumlu /chat/completions konuşan somut istemci.

    Sağlayıcıya özel hiçbir şey yok: base_url + api_key + model config'den gelir.
    429 / 5xx / bağlantı hatası -> exponential backoff (Retry-After başlığına uyar).
    """

    RETRY_STATUSES = {408, 409, 425, 429}
    # 200 gövdesinde string olarak gelen geçici hata adları (alt-string eşleşmesi, küçük harf).
    RETRY_CODE_NAMES = (
        "rate_limit", "ratelimit", "overloaded", "server_error",
        "service_unavailable", "timeout", "try_again",
    )

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

    def _retryable_code(self, code) -> bool:
        """200 gövdesindeki hata kodu geçici mi? int, sayısal string ya da bilinen hata adı."""
        if isinstance(code, bool):
            return False
        if isinstance(code, int):
            return self._retryable(code)
        if isinstance(code, str):
            c = code.strip()
            if c.isdigit():
                return self._retryable(int(c))
            cl = c.lower()
            return any(ad in cl for ad in self.RETRY_CODE_NAMES)
        return False

    def _retryable_body_error(self, err: dict) -> bool:
        """err.code, err.status, err.http_status alanlarından herhangi biri geçici ise True."""
        return any(self._retryable_code(err.get(k)) for k in ("code", "status", "http_status"))

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
    def _extract(data: dict) -> Yanit:
        choices = data.get("choices") or []
        if not choices:
            raise LLMError(f"yanıtta 'choices' yok: {str(data)[:300]}")
        secim = choices[0] if isinstance(choices[0], dict) else {}
        msg = secim.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):  # bazı sağlayıcılar parça listesi döndürür
            content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
        finish_reason = secim.get("finish_reason")
        if finish_reason is not None and not isinstance(finish_reason, str):
            finish_reason = str(finish_reason)
        # content boşsa reasoning_content/reasoning metin yerine KONMAZ; sadece işaretlenir.
        metin = content if isinstance(content, str) else ""
        return Yanit(metin=metin, finish_reason=finish_reason, bos_icerik=(metin == ""))

    # --- ana çağrı -----------------------------------------------------------
    def complete(self, messages: list[dict]) -> Yanit:
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
                            if isinstance(err, dict) and self._retryable_body_error(err):
                                code = err.get("code", err.get("status", err.get("http_status")))
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
