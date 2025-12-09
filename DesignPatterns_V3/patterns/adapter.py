"""Adapter: адаптирует внешние форматы изображений/метаданных под внутренний интерфейс.

Роль: обеспечивает совместимость сторонних библиотек/форматов с API приложения.
"""
from typing import Dict


class EXIFAdapter:
    """Простой адаптер для извлечения GPS и метаданных в единый формат."""

    @staticmethod
    def to_standard(exif_dict: Dict) -> Dict:
        # Преобразуем разные представления координат в единый формат
        gps = {}
        if not exif_dict:
            return gps
        # Поддержка как {'GPSLatitude':(...)} так и custom keys
        lat = exif_dict.get('GPSLatitude') or exif_dict.get('Latitude')
        lon = exif_dict.get('GPSLongitude') or exif_dict.get('Longitude')
        if lat and lon:
            gps['latitude'] = lat
            gps['longitude'] = lon
        # Копируем дополнительные поля, если есть
        for k in ('Make', 'Model', 'DateTime'):
            if k in exif_dict:
                gps[k.lower()] = exif_dict[k]
        return gps
