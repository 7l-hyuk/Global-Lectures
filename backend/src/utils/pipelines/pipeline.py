from src.utils.pipelines.base_stage import PipelineStage


class Pipeline:
    def __init__(self, stages: list[PipelineStage]):
        self.stages = stages

    def run(self, *args):
        current = args
        for stage in self.stages:
            current = stage.process(*current)
