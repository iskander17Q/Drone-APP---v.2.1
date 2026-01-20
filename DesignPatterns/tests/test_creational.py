"""Tests for Creational Patterns."""
import unittest
from patterns.creational import Singleton, AnimalFactory, CarBuilder


class TestSingleton(unittest.TestCase):
    def setUp(self):
        Singleton._instance = None

    def test_singleton_instance(self):
        a = Singleton(value=10)
        b = Singleton(value=20)
        self.assertIs(a, b)
        self.assertEqual(a.value, 10)

    def test_singleton_shared_state(self):
        s1 = Singleton(value=42)
        s2 = Singleton(value=100)
        self.assertEqual(s1.value, s2.value)


class TestFactory(unittest.TestCase):
    def test_dog_factory(self):
        dog = AnimalFactory.create('dog')
        self.assertEqual(dog.speak(), 'woof')

    def test_cat_factory(self):
        cat = AnimalFactory.create('cat')
        self.assertEqual(cat.speak(), 'meow')

    def test_unknown_animal(self):
        with self.assertRaises(ValueError):
            AnimalFactory.create('bird')


class TestBuilder(unittest.TestCase):
    def test_builder_chain(self):
        car = CarBuilder().add_engine('V8').add_wheels(4).build()
        self.assertEqual(car.engine, 'V8')
        self.assertEqual(car.wheels, 4)

    def test_builder_partial(self):
        car = CarBuilder().add_engine('V12').build()
        self.assertEqual(car.engine, 'V12')
        self.assertEqual(car.wheels, 0)


if __name__ == '__main__':
    unittest.main()
