import logging

import sapi.config.general

logger = logging.getLogger()

def _configure_console_log():
    ch = logging.StreamHandler()

    FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(FMT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if sapi.config.general.IS_DEBUG is True:
    _configure_console_log()
    logger.setLevel(logging.DEBUG)
