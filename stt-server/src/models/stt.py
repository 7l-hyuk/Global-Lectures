import whisperx

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import SttService

stt_service = SttService()


@stt_service.register_service("whisperX")
class WhisperxSttService(BaseServiceModel):
    def init_model(self):
        self.model = whisperx.load_model(
            whisper_arch="large-v2",
            device=device,
            language=self.language,
            compute_type="float16" if device == "cuda" else "int8"
        )
        self.aligned_model, self.metadata = whisperx.load_align_model(
            language_code=self.language,
            device=device
        )

    def process(self, audio_path: str):
        segments = self.model.transcribe(audio_path, language=self.language)["segments"]
        aligned: dict[str, dict] = whisperx.align(
            segments,
            self.aligned_model,
            self.metadata,
            audio_path,
            device
        )
        return aligned["segments"]
