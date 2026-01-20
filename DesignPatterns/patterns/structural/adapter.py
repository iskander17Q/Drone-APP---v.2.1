import logging

logger = logging.getLogger(__name__)


class OldLogger:
    def write(self, message):
        logger.info('OLD LOG: %s', message)


class LoggerAdapter:
    def __init__(self, old_logger):
        self.old = old_logger

    def log(self, msg):
        self.old.write(msg)


def run():
    old = OldLogger()
    adapted = LoggerAdapter(old)
    adapted.log('adapter run')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
