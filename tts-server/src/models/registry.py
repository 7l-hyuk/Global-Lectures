from typing import Literal
from dataclasses import dataclass

from src.models.basemodel import BaseServiceModel

ServiceModel = Literal["coqui-xtts-v2", "elevenlabs"]
LanguageCode = Literal["ko", "en", "ja", "zh"]


@dataclass
class TTSService:
    SUPPORTED_LANGUAGE = {
        "ko": "ko",
        "en": "en",
        "ja": "ja",
        "zh": "zh"
    }
    SERVICE_MODEL_REGISTRY = {}

    def register_service(self, name: str):
        def decorator(cls):
            self.SERVICE_MODEL_REGISTRY[name] = cls
            return cls
        return decorator

    def create_service(
            self, 
            name: ServiceModel,
            target_lang: LanguageCode,
        ) -> BaseServiceModel:
        cls = self.SERVICE_MODEL_REGISTRY.get(name)
        if cls is None:
            raise ValueError(f"Service model '{name}' is not registered")
        return cls(
            support_language=self.SUPPORTED_LANGUAGE,
            target_lang=target_lang
        )
