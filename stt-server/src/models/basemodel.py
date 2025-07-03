from abc import ABC, abstractmethod
from dataclasses import dataclass

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


@dataclass
class BaseServiceModel(ABC):
    language: str
    support_language: dict[str, str]

    def __post_init__(self):
        self.language = self.support_language[self.language]      

    def run(self, audio_path: str):
        self.init_model()
        return self.process(audio_path=audio_path)

    @abstractmethod
    def init_model(self):
        ...

    @abstractmethod
    def process(self, audio_path: str):
        ...
