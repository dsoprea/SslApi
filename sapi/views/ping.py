import logging

_logger = logging.getLogger(__name__)


class PingView(object):
    def GET(self):
        _logger.debug("Ping.")
        return ''
