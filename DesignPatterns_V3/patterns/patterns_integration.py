"""Инициализация всех паттернов и создание реестра для использования в приложении.

Регистрирует совместимые функции из существующего кода (image_processing, utils)
и возвращает словарь с удобными объектами/фасадами/стратегиями.
"""
from .singleton import ConfigManager
from .factory import AnalysisFactory
from .builder import ReportBuilder
from .adapter import EXIFAdapter
from .decorator import timed, logged
from .facade import AnalysisFacade
from .strategy import ThresholdClassifier, KMeansClassifier
from .observer import Event
from .command import AnalyzeCommand, SaveReportCommand


def initialize_patterns():
    registry = {}

    # Singleton: глобальная конфигурация
    config = ConfigManager()
    config.set('initialized_at', __import__('datetime').datetime.utcnow().isoformat())
    registry['config'] = config

    # Factory: регистрируем базовый набор обработчиков
    factory = AnalysisFactory()
    try:
        from image_processing import load_image as _load_image
        from image_processing import compute_indices as _compute_indices
        from image_processing import generate_heatmap as _generate_heatmap
    except Exception:
        # Безопасно: если image_processing недоступен — регистрируем заглушки
        _load_image = lambda p: None
        _compute_indices = lambda img: {}
        _generate_heatmap = lambda *a, **k: None

    factory.register('default', lambda: (_load_image, _compute_indices, _generate_heatmap))
    registry['factory'] = factory

    # Facade: удобная точка запуска анализа
    loaders = {
        'image_loader': _load_image,
        'compute_indices': _compute_indices,
        'generate_heatmap': _generate_heatmap,
    }
    facade = AnalysisFacade(loaders)
    registry['facade'] = facade

    # Strategy: добавляем варианты классификации
    registry['strategy_threshold'] = ThresholdClassifier()
    registry['strategy_kmeans'] = KMeansClassifier()

    # Observer: событие завершения анализа
    registry['on_analysis_done'] = Event()

    # Commands: фабрика команд
    registry['commands'] = {
        'AnalyzeCommand': AnalyzeCommand,
        'SaveReportCommand': SaveReportCommand
    }

    # Документ-Builder
    registry['report_builder'] = ReportBuilder

    # Адаптер EXIF
    registry['exif_adapter'] = EXIFAdapter

    # Декораторы
    registry['decorators'] = {'timed': timed, 'logged': logged}

    return registry
