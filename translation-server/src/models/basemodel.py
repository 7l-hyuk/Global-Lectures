from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.schema import SubtitleEntry

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


@dataclass
class BaseServiceModel(ABC):
    source_lang: str
    target_lang: str
    support_language: dict[str, str]

    def __post_init__(self):
        self.source_lang = self.support_language[self.source_lang]    
        self.target_lang = self.support_language[self.target_lang]

    def run(self, subtitles: list[SubtitleEntry]):
        self.init_model()
        return self.process(subtitles=subtitles)

    @abstractmethod
    def init_model(self):
        ...

    @abstractmethod
    def process(self, subtitles: list[SubtitleEntry]):
        ...
