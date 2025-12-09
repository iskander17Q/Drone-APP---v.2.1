"""Creational Patterns: Singleton, Factory, Builder."""
from .singleton import Singleton
from .factory import AnimalFactory, Dog, Cat, Animal
from .builder import CarBuilder, Car

__all__ = [
    'Singleton',
    'AnimalFactory', 'Animal', 'Dog', 'Cat',
    'CarBuilder', 'Car',
]
