import torch
import soundfile
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import register_service
from src.utils.audio.audio import audio_sync
from src.utils.logger import logger


@register_service("tts")
class TTSSeviceModel(BaseServiceModel):
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

    def process(self, segments):
        tts_audio = self.userpath.tts_audio
        tts_audio_sync = self.userpath.tts_audio_sync

        for i, segment in enumerate(segments):
            file_name = f"{i:03d}.wav"
            file_path = tts_audio / file_name
            
            logger.info(segment["text"])

            self.model.tts_to_file(
                text=segment["text"],
                speaker_wav=self.userpath.reference_speaker,
                language=self.language[0],
                file_path=file_path,
            )
            audio, samplerate = soundfile.read(file_path)
            duration = len(audio) / samplerate
            tar_duration = segment["end"] - segment["start"]
            segment["file"] = tts_audio_sync / file_name
            audio_sync(
                file_path,
                segment["file"],
                speed=duration / tar_duration
            )
