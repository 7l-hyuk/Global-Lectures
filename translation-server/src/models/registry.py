from typing import Literal
from dataclasses import dataclass

from src.models.basemodel import BaseServiceModel

ServiceModel = Literal["NLLB-200", "GPT-3.5-turbo"]
LanguageCode = Literal["ko", "en", "ja", "zh"]


@dataclass
class TranslationService:
    SUPPORTED_LANGUAGE = {
        "ko": "kor_Hang",
        "en": "eng_Latn",
        "ja": "jpn_Jpan",
        "zh": "zho_Hans"
    }
    SERVICE_MODEL_REGISTRY = {}

    def register_service(self, name: str):
        def decorator(cls):
            self.SERVICE_MODEL_REGISTRY[name] = cls
            return cls
        return decorator

    def create_service(self, name: ServiceModel, source_lang: LanguageCode, target_lang: LanguageCode) -> BaseServiceModel:
        cls = self.SERVICE_MODEL_REGISTRY.get(name)
        if cls is None:
            raise ValueError(f"Service model '{name}' is not registered")
        return cls(
            support_language=self.SUPPORTED_LANGUAGE,
            source_lang=source_lang,
            target_lang=target_lang
        )
