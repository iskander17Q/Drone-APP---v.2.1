"""Command: инкапсулирует операции (анализ, экспорт) как объекты команд."""
from typing import Protocol, Any


class Command(Protocol):
    def execute(self) -> Any:
        ...


class AnalyzeCommand:
    def __init__(self, facade, image_path, export_folder=None):
        self.facade = facade
        self.image_path = image_path
        self.export_folder = export_folder

    def execute(self):
        return self.facade.run_full_analysis(self.image_path, self.export_folder)


class SaveReportCommand:
    def __init__(self, generate_pdf_fn, pdf_path, image_path, heatmap_path, text_report, gps):
        self.generate_pdf_fn = generate_pdf_fn
        self.pdf_path = pdf_path
        self.image_path = image_path
        self.heatmap_path = heatmap_path
        self.text_report = text_report
        self.gps = gps

    def execute(self):
        return self.generate_pdf_fn(
            self.pdf_path, self.image_path, self.heatmap_path, self.text_report, self.gps
        )
