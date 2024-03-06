from .step import Step
from yt_concate.yt_logging import generate_logger


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = generate_logger()
        logger.info('in Postflight')
        if inputs['cleanup']:
            utils.delete_dirs()