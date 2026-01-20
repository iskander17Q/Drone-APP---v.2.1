"""Structural Patterns: Adapter, Decorator, Facade."""
from .adapter import LoggerAdapter, OldLogger
from .decorator import make_bold, greet
from .facade import Facade, SubsystemA, SubsystemB

__all__ = [
    'LoggerAdapter', 'OldLogger',
    'make_bold', 'greet',
    'Facade', 'SubsystemA', 'SubsystemB',
]
