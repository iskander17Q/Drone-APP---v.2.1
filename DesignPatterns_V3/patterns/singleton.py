"""Singleton: единичный менеджер конфигурации для приложения.

Роль: хранит глобальные настройки/контекст, доступный из разных частей
приложения без создания множества экземпляров.
"""
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        # Потокобезопасная инициализация единственного экземпляра
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):
    """Простой конфиг-менеджер, используемый как Singleton.

    Хранит словарь настроек и предоставляет безопасный доступ.
    """

    def __init__(self):
        self._config = {}

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value

    def as_dict(self):
        return dict(self._config)
