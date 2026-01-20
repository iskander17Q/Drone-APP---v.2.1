"""Factory: создание обработчиков экспорта/анализа по типу запроса.

Роль: предоставляет простой API для получения конкретных реализаций
функций экспорта/анализа в зависимости от конфигурации или типа данных.
"""
from typing import Callable, Dict


class AnalysisHandler:
    def __init__(self, func: Callable):
        self.func = func

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class AnalysisFactory:
    """Регистрирует и создаёт обработчики анализа по имени."""

    def __init__(self):
        self._registry: Dict[str, Callable] = {}

    def register(self, name: str, constructor: Callable):
        self._registry[name] = constructor

    def create(self, name: str, *args, **kwargs) -> AnalysisHandler:
        constructor = self._registry.get(name)
        if not constructor:
            raise ValueError(f"Unknown analysis handler: {name}")
        return AnalysisHandler(constructor(*args, **kwargs))
