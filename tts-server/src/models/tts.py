from io import BytesIO

import torch
import soundfile as sf
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import TTSService

tts_service = TTSService()
    

@tts_service.register_service("coqui-xtts-v2")
class CoquiTtsService(BaseServiceModel):
    def init_model(self):
        torch.serialization.add_safe_globals(
            [
                XttsConfig,
                XttsAudioConfig,
                BaseDatasetConfig,
                XttsArgs
            ]
        )
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    def process(
            self,
            text: str,
            speaker_wav: str
        ) -> tuple[list[int], float]:
            buffer = BytesIO()

            wav = self.model.tts(
                text=text,
                language=self.target_lang,
                speaker_wav=speaker_wav
            )
            sample_rate = self.model.synthesizer.tts_config.audio["sample_rate"]
            audio_time = len(wav) / sample_rate
            print(sample_rate)
            sf.write(buffer, wav, sample_rate, format="WAV")
            buffer.seek(0)
            return buffer, audio_time

