# Design Patterns

Полная реализация девяти паттернов проектирования, организованная по категориям: Creational, Structural, Behavioral.

## Структура

```
patterns/
├── creational/          # Паттерны создания объектов
│   ├── singleton.py     # Одиночка
│   ├── factory.py       # Фабрика
│   └── builder.py       # Строитель
├── structural/          # Структурные паттерны
│   ├── adapter.py       # Адаптер
│   ├── decorator.py     # Декоратор
│   └── facade.py        # Фасад
└── behavioral/          # Поведенческие паттерны
    ├── strategy.py      # Стратегия
    ├── observer.py      # Наблюдатель
    └── command.py       # Команда

tests/                   # Тесты для всех паттернов
docs/                    # Документация
└── README.md           # Этот файл
```

## Использование

### Импорт паттернов

```python
# Creational Patterns
from patterns.creational import Singleton, AnimalFactory, CarBuilder

# Structural Patterns
from patterns.structural import LoggerAdapter, make_bold, Facade

# Behavioral Patterns
from patterns.behavioral import Sorter, BubbleSort, Subject, Light, Switch
```

### Запуск модуля напрямую

Каждый модуль оснащён функцией `run()` для быстрой проверки:

```bash
python patterns/creational/singleton.py
python patterns/structural/facade.py
python patterns/behavioral/strategy.py
```

## Тестирование

Запуск всех тестов:

```bash
python -m pytest tests/
# или
cd tests && python __init__.py
```

Запуск тестов отдельной категории:

```bash
python -m pytest tests/test_creational.py
python -m pytest tests/test_structural.py
python -m pytest tests/test_behavioral.py
```

## Документация

Подробное описание каждого паттерна находится в папке `docs/`:

- [Creational Patterns](docs/CREATIONAL.md) — Singleton, Factory, Builder
- [Structural Patterns](docs/STRUCTURAL.md) — Adapter, Decorator, Facade
- [Behavioral Patterns](docs/BEHAVIORAL.md) — Strategy, Observer, Command

## Интеграция

Модули готовы к использованию в основном приложении. Для интеграции в проект `Monolith` или `Microservice`:

```python
# В вашем коде
from patterns.behavioral import Strategy, Sorter, BubbleSort

class CustomStrategy(Strategy):
    def sort(self, data):
        return sorted(data, reverse=True)

sorter = Sorter(CustomStrategy())
result = sorter.perform([3, 1, 2])
```

## Разработка

Все модули следуют соглашениям:

- Используют `logging` вместо `print` для вывода.
- Каждый модуль предоставляет функцию `run()` для проверки работоспособности.
- `__init__.py` файлы каждой категории экспортируют публичные классы и функции.
- Каждый паттерн сопровождается unit-тестами.
