import logging

logger = logging.getLogger(__name__)


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, obs):
        self._observers.append(obs)

    def notify(self, msg):
        for o in self._observers:
            o.update(msg)


class PrintObserver:
    def update(self, msg):
        logger.info('Observer received: %s', msg)


def run():
    s = Subject()
    s.attach(PrintObserver())
    s.notify('event')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
