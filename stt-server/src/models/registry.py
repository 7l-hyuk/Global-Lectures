from typing import Literal
from dataclasses import dataclass

from src.models.basemodel import BaseServiceModel

ServiceModel = Literal["whisperX", "elevenlabs"]


@dataclass
class SttService:
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

    def create_service(self, name: ServiceModel, language: str) -> BaseServiceModel:
        cls = self.SERVICE_MODEL_REGISTRY.get(name)
        if cls is None:
            raise ValueError(f"Service model '{name}' is not registered")
        return cls(
            support_language=self.SUPPORTED_LANGUAGE,
            language=language
        )
