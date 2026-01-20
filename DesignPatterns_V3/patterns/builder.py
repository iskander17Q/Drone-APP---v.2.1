"""Builder: пошаговая сборка сложных объектов отчёта/экспорта.

Роль: гибко настраивать содержимое PDF-отчёта и набора экспортируемых файлов.
"""
from typing import List, Dict


class ReportBuilder:
    def __init__(self):
        self._parts: List[str] = []
        self._meta: Dict[str, str] = {}

    def set_title(self, title: str):
        self._meta['title'] = title
        return self

    def add_section(self, heading: str, body: str):
        self._parts.append(f"{heading}\n{body}")
        return self

    def set_author(self, author: str):
        self._meta['author'] = author
        return self

    def build(self) -> Dict[str, object]:
        return {
            'meta': dict(self._meta),
            'content': '\n\n'.join(self._parts)
        }
