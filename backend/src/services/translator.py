from dataclasses import dataclass
from pathlib import Path

import httpx



@dataclass
class TranslatorClient:
    API_URL: str

    def run(
        self,
        subtitles: list[dict],
        source_lang: str,
        target_lang: str,
        model: str,
        timeout: float = 180.0
    ) -> dict:
        payload = {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "model": model,
            "subtitles": subtitles
        }
        return httpx.post(
            self.API_URL,
            json=payload,
            timeout=timeout
        ).json()
