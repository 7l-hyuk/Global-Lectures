from io import BytesIO

import torch
import soundfile
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import register_service
from src.utils.audio import audio
from src.utils.logger import logger
from src.config import service_settings


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
            # audio, samplerate = soundfile.read(file_path)
            # duration = len(audio) / samplerate
            tar_duration = segment["end"] - segment["start"]
            segment["file"] = tts_audio_sync / file_name
            audio.audio_sync(
                file_path,
                segment["file"],
                speed=audio.length(file_path) / tar_duration
            )
        return None


@register_service("tts-elevenlabs")
class TTSSeviceModel(BaseServiceModel):
    def init_model(self):
        self.elevenlabs = ElevenLabs(api_key=service_settings.XI_API_KEY)        

    def process(self, segments: dict, voice_id: str | None = None):
        tts_audio = self.userpath.tts_audio
        tts_audio_sync = self.userpath.tts_audio_sync
        segment_len = len(segments)

        if not voice_id:
            voice = self.elevenlabs.voices.ivc.create(
                name=str(self.userpath.user.name),
                files=[BytesIO(open(str(self.userpath.reference_speaker), "rb").read())]
            )
            voice_id = voice.voice_id

        for i, segment in enumerate(segments):
            file_name = f"{i:03d}.mp3"
            file_path = tts_audio / file_name

            previous_text = segments[i - 1]["text"] if i > 1 else None
            next_text = segments[i + 1]["text"] if i < segment_len - 1 else None

            response = self.elevenlabs.text_to_speech.convert(
                text=segment["text"],
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
                previous_text=previous_text,
                next_text=next_text,
            )

            with open(file_path, "wb") as f:
                for chunk in response:
                    if chunk:
                        f.write(chunk)
            
            # audio, samplerate = soundfile.read(file_path)
            # duration = len(audio) / samplerate
            tar_duration = segment["end"] - segment["start"]
            segment["file"] = tts_audio_sync / file_name

            try:
                audio.audio_sync(
                    file_path,
                    segment["file"],
                    speed=audio.length(file_path) / tar_duration
                )
            except Exception as e:
                print(e)
                return 
        return voice_id
