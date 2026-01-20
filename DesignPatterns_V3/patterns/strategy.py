"""Strategy: разные алгоритмы классификации/порогов можно переключать во время рантайма."""
from typing import Protocol, Any


class ClassifyStrategy(Protocol):
    def classify(self, index_map: Any) -> dict:
        ...


class ThresholdClassifier:
    def __init__(self, healthy_thresh=0.5, stress_thresh=0.2):
        self.healthy = healthy_thresh
        self.stress = stress_thresh

    def classify(self, index_map):
        total = index_map.size
        healthy = (index_map >= self.healthy).sum() / total * 100
        stressed = ((index_map < self.healthy) & (index_map >= self.stress)).sum() / total * 100
        dead = (index_map < self.stress).sum() / total * 100
        return {'healthy': healthy, 'stressed': stressed, 'dead': dead}


class KMeansClassifier:
    def __init__(self, k=3):
        self.k = k

    def classify(self, index_map):
        # Лёгкая реализация: используем numpy для грубой кластеризации
        import numpy as np
        vals = index_map.flatten()
        # Разбиваем на k равных интервалов
        bins = np.linspace(vals.min(), vals.max(), self.k + 1)
        total = vals.size
        res = {}
        for i in range(self.k):
            mask = (vals >= bins[i]) & (vals < bins[i+1])
            res[f'cluster_{i}'] = mask.sum() / total * 100
        return res
