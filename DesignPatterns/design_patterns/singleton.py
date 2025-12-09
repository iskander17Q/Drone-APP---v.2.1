import logging

logger = logging.getLogger(__name__)


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = kwargs.get('value', 0)
        return cls._instance


def run():
    a = Singleton(value=10)
    b = Singleton(value=20)
    logger.info('a.value %s', a.value)
    logger.info('b.value %s', b.value)
    logger.info('a is b -> %s', a is b)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
