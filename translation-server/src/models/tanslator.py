from transformers import pipeline

from src.models.basemodel import BaseServiceModel, device
from src.models.registry import TranslationService
from src.schema import SubtitleEntry

translation_service = TranslationService()

@translation_service.register_service("NLLB-200")
class WhisperxSttService(BaseServiceModel):
    def init_model(self):
        self.model = pipeline(
            task="translation",
            model="facebook/nllb-200-distilled-600M",
            src_lang=self.source_lang,
            tgt_lang=self.target_lang,
            max_length=512
        )

    def process(self, subtitles: list[SubtitleEntry]) -> list[SubtitleEntry]:
        for sub in subtitles:
            sub.text = self.model(sub.text, max_length=512)[0]['translation_text']
        return subtitles
