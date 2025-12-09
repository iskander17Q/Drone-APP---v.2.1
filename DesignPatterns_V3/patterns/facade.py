"""Facade: упрощённый интерфейс для запуска полного анализа и экспорта.

Роль: скрыть сложную логику из `main.py` и предоставить удобный метод
`run_full_analysis` для использования в UI и командах.
"""
import os
from .singleton import ConfigManager
from .builder import ReportBuilder
from .decorator import timed


class AnalysisFacade:
    def __init__(self, loaders):
        self.loaders = loaders
        self.config = ConfigManager()

    @timed
    def run_full_analysis(self, image_path, export_folder=None):
        # Используем стандартизованные загрузчики и билдера отчёта
        loader = self.loaders.get('image_loader')
        if not loader:
            raise RuntimeError('No image loader configured')
        image = loader(image_path)

        compute = self.loaders.get('compute_indices')
        indices = compute(image)

        # Строим базовый отчёт
        builder = ReportBuilder()
        builder.set_title('Анализ поля').add_section('Индексы', 'Сгенерированы индексы').set_author('DroneAPP')

        # Экспорт тепловой карты
        if export_folder:
            os.makedirs(export_folder, exist_ok=True)
            heatmap_path = os.path.join(export_folder, 'heatmap_from_facade.png')
            gen = self.loaders.get('generate_heatmap')
            gen(indices.get('NDVI_emp') or list(indices.values())[0], heatmap_path)
        else:
            heatmap_path = None

        return {
            'report': builder.build(),
            'heatmap': heatmap_path,
            'indices': indices
        }
