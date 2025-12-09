import logging

logger = logging.getLogger(__name__)


class SubsystemA:
    def operation(self):
        return 'A'


class SubsystemB:
    def operation(self):
        return 'B'


class Facade:
    def __init__(self):
        self.a = SubsystemA()
        self.b = SubsystemB()

    def do_work(self):
        return f'Facade: {self.a.operation()} + {self.b.operation()}'


def run():
    f = Facade()
    logger.info('%s', f.do_work())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
