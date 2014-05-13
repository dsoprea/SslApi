import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

ch = logging.StreamHandler()

FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(FMT)
ch.setFormatter(formatter)
logger.addHandler(ch)
