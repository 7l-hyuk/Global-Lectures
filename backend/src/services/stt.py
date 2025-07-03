from dataclasses import dataclass
from pathlib import Path

import httpx


@dataclass
class SttClient:
    API_URL: str

    def run(
        self,
        audio_path: Path,
        language: str,
        model: str,
        timeout: float = 180.0
    ) -> dict:
        payload = {
            "audio_path": str(audio_path),
            "language": language,
            "model": model
        }
        return httpx.post(
            self.API_URL,
            json=payload,
            timeout=timeout
        ).json()
