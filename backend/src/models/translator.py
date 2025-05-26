from typing import Any

from transformers import pipeline

from src.models.basemodel import BaseServiceModel
from src.models.registry import register_service
from src.utils.logger import logger


@register_service("translator")
class TranslationServiceModel(BaseServiceModel):
    def init_model(self):
        self.model = pipeline(
            task="translation",
            model="facebook/nllb-200-distilled-600M",
            src_lang=self.language[0],
            tgt_lang=self.language[1],
            max_length=512
        )

    def process(self, segments: list[dict[str, Any]]):
        for segment in segments:
            logger.info(segment["text"])
            segment["text"] = self.model(
                segment["text"],
                max_length=512
            )[0]["translation_text"]
            logger.info(segment["text"])
