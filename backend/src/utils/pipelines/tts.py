import os
from dataclasses import dataclass
from contextlib import contextmanager
from pathlib import Path
from enum import Enum

import httpx

from src.config import api_settings


class TtsTask(Enum):
    VOICE_ID_GENERATION = 1
    DELETE_VOICE_ID = 2
    TTS = 3


@dataclass
class TtsClient:
    API_URL: str = api_settings.TTS_SERVER_URL
    voice_id: str | None = None

    def _get_api_url(self, task: TtsTask):
        match task:
            case TtsTask.VOICE_ID_GENERATION:
                return self.API_URL + "voice-id"
            case TtsTask.VOICE_ID_GENERATION:
                return self.API_URL + "voice-id"
            case TtsTask.TTS:
                return self.API_URL + "tts"

    @contextmanager
    def _generate_voice_id(self, speaker_wav: Path):
        with httpx.Client() as client:
            with open(speaker_wav, "rb") as f:
                res = client.post(
                    self._get_api_url(TtsTask.VOICE_ID_GENERATION),
                    files={"speaker_wav": f},
                    timeout=5
                )
        if res.status_code != 200:
            pass

        voice_id = res.json()["voice_id"]
        yield voice_id

        with httpx.Client() as client:
            res = client.delete(
                self._get_api_url(TtsTask.VOICE_ID_GENERATION)
                + f"?voice_id={voice_id}",
            )

    def run(
        self,
        texts: list[str],
        target_lang: str,
        model: str,
        speaker_wav: Path,
        output: Path,
        timeout: float = 180.0
    ):
        os.makedirs(output, exist_ok=True)
        with self._generate_voice_id(speaker_wav) as voice_id:
            with httpx.Client() as client:
                for i, text in enumerate(texts):
                    payload = {
                        "target_lang": target_lang,
                        "model": model,
                        "text": text,
                        "voice_id": voice_id
                    }
                    res = client.post(
                        self._get_api_url(task=TtsTask.TTS),
                        data=payload,
                        timeout=timeout
                    )
                    with open(output / f"{i:03d}.wav", "wb") as out:
                        for chunk in res.iter_bytes(1024*1024):
                            if chunk:
                                out.write(chunk)
