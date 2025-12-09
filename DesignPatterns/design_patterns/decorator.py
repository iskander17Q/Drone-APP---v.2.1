import logging

logger = logging.getLogger(__name__)


def make_bold(fn):
    def wrapper(*args, **kwargs):
        return '<b>' + fn(*args, **kwargs) + '</b>'
    return wrapper


@make_bold
def greet(name):
    return f'Hello, {name}'


def run():
    result = greet('World')
    logger.info('%s', result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
