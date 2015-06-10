import os
import logging
import logging.handlers

_LOGGER = logging.getLogger()

_IS_DEBUG = bool(int(os.environ.get('DEBUG', '0')))
_DO_DEBUG_SCREEN_LOG = bool(int(os.environ.get('DO_DEBUG_SCREEN_LOG', '0')))
_SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL0

def _configure_logs():
    logger = logging.getLogger()

    if _IS_DEBUG is True or _DO_DEBUG_SCREEN_LOG is True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Configure screen.
    if _IS_DEBUG is True or _DO_DEBUG_SCREEN_LOG is True:
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(format)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # Configure Syslog.
    if os.path.exists('/dev/log') is True:
        format = '%(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(format)

        sh2 = logging.handlers.SysLogHandler(
                address='/dev/log',
                facility=_SYSLOG_FACILITY)

        sh2.setFormatter(formatter)
        logger.addHandler(sh2)

_configure_logs()
