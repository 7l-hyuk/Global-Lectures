from abc import ABC, abstractmethod
from dataclasses import dataclass

import torch

from src.utils.path import UserPath

device = "cuda" if torch.cuda.is_available() else "cpu"


@dataclass
class BaseServiceModel(ABC):
    userpath: UserPath | None
    language: list[str]
    support_language_code: dict[str, str]

    def __post_init__(self):
        for i, language in enumerate(self.language):
            self.language[i] = self.support_language_code[language]
    
    def run(self, *args, **kwargs):
        self.init_model()
        return self.process(*args, **kwargs)

    @abstractmethod
    def init_model(self):
        ...

    @abstractmethod
    def process(self, *args, **kwargs):
        ...
