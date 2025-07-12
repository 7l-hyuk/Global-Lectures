from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


@dataclass
class BaseServiceModel(ABC):
    target_lang: str
    support_language: dict[str, str]

    def __post_init__(self):
        self.target_lang = self.support_language[self.target_lang]

    def run(
            self,
            text: str,
            speaker_wav: str
        ):
        self.init_model()
        return self.process(
            text=text,
            speaker_wav=speaker_wav
        )

    @abstractmethod
    def init_model(self):
        ...

    @abstractmethod
    def process(
        self,
        text: str,
        speaker_wav: str
    ):
        ...
