from .step import Step
from yt_concate.yt_logging import generate_logger


class Preflight(Step):
    def process(self, data, inputs, utils):
        logger = generate_logger()
        logger.info('in Preflight')
        utils.create_dirs()
