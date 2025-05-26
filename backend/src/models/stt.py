import whisperx

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import register_service


@register_service("stt")
class STTServiceModel(BaseServiceModel):
    def init_model(self):
        self.model = whisperx.load_model(
            whisper_arch="large-v2",
            device=device,
            compute_type="float16" if device == "cuda" else "int8"
        )
        self.aligned_model, self.metadata = whisperx.load_align_model(
            language_code=self.language[0],
            device=device
        )

    def process(self):
        audio = str(self.userpath.reference_speaker)
        segments = self.model.transcribe(audio, language=self.language[0])["segments"]
        aligned: dict[str, dict] = whisperx.align(
            segments,
            self.aligned_model,
            self.metadata,
            audio,
            device
        )
        return aligned["segments"]