"""config/models.yaml + .env yükleme."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Defaults:
    temperature: float = 0.7
    max_tokens: int = 1024
    timeout: float = 90.0
    max_retries: int = 8
    max_turns: int = 15


@dataclass
class SubjectConfig:
    id: str
    base_url: str
    model: str
    api_key_env: str
    temperature: float | None = None
    max_tokens: int | None = None
    extra_headers: dict = field(default_factory=dict)
    extra_body: dict = field(default_factory=dict)


def load_dotenv(path: Path) -> None:
    """Bağımlılık eklememek için minimal .env okuyucu. Mevcut env değişkenlerini ezmez."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def load_config(path: Path) -> tuple[Defaults, list[SubjectConfig]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    defaults = Defaults(**(data.get("defaults") or {}))
    subjects = [SubjectConfig(**raw) for raw in (data.get("subjects") or [])]
    if not subjects:
        raise SystemExit(f"{path}: 'subjects' boş")
    ids = [s.id for s in subjects]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"{path}: tekrar eden subject id")
    return defaults, subjects
