from abc import ABC, abstractmethod


class PipelineStage(ABC):
    @abstractmethod
    def process(self):
        pass
