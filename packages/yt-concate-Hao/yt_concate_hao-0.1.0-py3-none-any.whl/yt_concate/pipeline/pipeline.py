from yt_concate.pipeline.steps.step import StepException
from yt_concate.yt_logging import generate_logger


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, inputs, utils):
        logger = generate_logger()
        data = None
        for step in self.steps:
            try:
                data = step.process(data, inputs, utils)
            except StepException as e:
                logger.error('Exception happened:', e)
                break
