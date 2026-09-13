"""results/runs.jsonl + results/transcripts/ yazımı ve devam (resume) desteği."""
from __future__ import annotations

import json
from pathlib import Path


class Recorder:
    def __init__(self, out_dir: Path):
        self.out_dir = out_dir
        self.runs_path = out_dir / "runs.jsonl"
        self.tr_dir = out_dir / "transcripts"
        self.tr_dir.mkdir(parents=True, exist_ok=True)

    def mevcut_anahtarlar(self) -> set[tuple[str, str, int]]:
        if not self.runs_path.is_file():
            return set()
        keys = set()
        for line in self.runs_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            keys.add((r["model_id"], r["kosul"], r["run_no"]))
        return keys

    def kayitlar(self) -> list[dict]:
        if not self.runs_path.is_file():
            return []
        return [
            json.loads(l)
            for l in self.runs_path.read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]

    @staticmethod
    def transcript_adi(model_id: str, kosul: str, run_no: int) -> str:
        return f"{model_id}__{kosul}__{run_no:03d}.json"

    def kaydet(self, ozet: dict, transcript: dict) -> Path:
        tr_path = self.tr_dir / self.transcript_adi(ozet["model_id"], ozet["kosul"], ozet["run_no"])
        tr_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8")
        ozet = {**ozet, "transcript_dosyasi": str(tr_path.relative_to(self.out_dir)).replace("\\", "/")}
        with self.runs_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ozet, ensure_ascii=False) + "\n")
        return tr_path
