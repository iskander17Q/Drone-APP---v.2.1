"""Observer: уведомление подписчиков о статусах задач анализа."""
from typing import Callable, List


class Event:
    def __init__(self):
        self._subscribers: List[Callable] = []

    def subscribe(self, fn: Callable):
        if fn not in self._subscribers:
            self._subscribers.append(fn)

    def unsubscribe(self, fn: Callable):
        if fn in self._subscribers:
            self._subscribers.remove(fn)

    def notify(self, *args, **kwargs):
        for fn in list(self._subscribers):
            try:
                fn(*args, **kwargs)
            except Exception:
                pass
