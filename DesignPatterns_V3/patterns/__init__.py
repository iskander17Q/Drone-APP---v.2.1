"""Пакет с реализациями дизайн-паттернов для интеграции в приложение.

Здесь держится точка входа `initialize_patterns`, которая собирает
все реализации и возвращает реестр/контекст для дальнейшего использования.
"""

from .patterns_integration import initialize_patterns  # noqa: F401

__all__ = ["initialize_patterns"]
