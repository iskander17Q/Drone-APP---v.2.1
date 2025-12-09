import logging

logger = logging.getLogger(__name__)


class Car:
    def __init__(self):
        self.engine = None
        self.wheels = 0

    def __repr__(self):
        return f"Car(engine={self.engine}, wheels={self.wheels})"


class CarBuilder:
    def __init__(self):
        self.car = Car()

    def add_engine(self, engine):
        self.car.engine = engine
        return self

    def add_wheels(self, n):
        self.car.wheels = n
        return self

    def build(self):
        return self.car


def run():
    car = CarBuilder().add_engine('V8').add_wheels(4).build()
    logger.info('%s', car)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
