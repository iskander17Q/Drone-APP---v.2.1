# Drone Image Analysis System - Design Patterns Application

Полнофункциональное приложение для анализа изображений с дрона, демонстрирующее все 9 паттернов проектирования в едином интегрированном решении.

## Что это?

Это рабочее приложение, а не набор отдельных примеров. Все 9 паттернов работают вместе в единой системе анализа данных дрона:

- **Creational**: Singleton (конфигурация), Factory (создание дронов), Builder (конструирование наборов данных)
- **Structural**: Adapter (интеграция логгеров), Decorator (добавление функциональности), Facade (упрощение взаимодействия)
- **Behavioral**: Strategy (выбор алгоритма сортировки), Observer (мониторинг событий), Command (управление операциями)

## Быстрый старт

### GUI режим (новый интегрированный интерфейс)

```bash
python3 run.py
# или
python3 run.py --ui
```

Графический интерфейс, который показывает все 9 паттернов в действии:
- Выбор типа дрона и количества изображений
- Визуализация всех активных паттернов
- Отслеживание событий системы (Observer)
- Отображение конфигурации (Singleton)

### CLI режим (интерактивное меню)

```bash
python3 run.py --cli
# или
python3 application.py
```

Интерактивное текстовое меню для анализа изображений.

### Автоматическая демонстрация (CLI)

```bash
python3 run.py --auto
# или
python3 application.py --auto
```

Система автоматически выполнит анализ с несколькими типами дронов.

### Запуск с оригинальным PyQt5 интерфейсом (если доступен)

```bash
python3 run.py --legacy
```

Запускает оригинальный полнофункциональный PyQt5 интерфейс из `main.py`.

## Как работает приложение

Приложение состоит из единого модуля `application.py`, который интегрирует все 9 паттернов:

### Главные компоненты

1. **DroneAPP** — главный класс приложения, орхестрирует все паттерны
2. **ImageProcessingConfig** (Singleton) — единая конфигурация системы
3. **DroneFactory** (Factory) — создаёт объекты разных типов дронов
4. **DroneDataBuilder** (Builder) — конструирует сложные наборы данных
5. **AnalysisFacade** (Facade) — упрощает взаимодействие с системой анализа
6. **LoggerAdapter** (Adapter) — адаптирует старую логгер-систему к новой
7. **ProcessingDecorator** (Decorator) — добавляет метаданные к сообщениям
8. **SystemObserver** (Observer) — мониторит события системы в реальном времени
9. **ImageProcessingCommand** (Command) — инкапсулирует операции обработки

### Процесс анализа

```
DroneAPP (главное приложение)
    ├── ImageProcessingConfig (Singleton) → единая конфигурация
    ├── DroneFactory (Factory) → создание дронов
    ├── DroneDataBuilder (Builder) → построение данных
    ├── AnalysisFacade (Facade) → упрощение взаимодействия
    │   ├── LoggerAdapter (Adapter) → адаптация логгеров
    │   ├── ProcessingDecorator (Decorator) → добавление метаданных
    │   └── Sorter + Strategy → выбор алгоритма сортировки
    ├── SystemObserver (Observer) → мониторинг событий
    └── ImageProcessingCommand (Command) → управление операциями
```

## Структура проекта

```
DesignPatterns/
├── application.py              # Главное приложение - интеграция всех паттернов
├── patterns/
│   ├── creational/            # Паттерны создания объектов
│   │   ├── singleton.py
│   │   ├── factory.py
│   │   └── builder.py
│   ├── structural/            # Структурные паттерны
│   │   ├── adapter.py
│   │   ├── decorator.py
│   │   └── facade.py
│   └── behavioral/            # Поведенческие паттерны
│       ├── strategy.py
│       ├── observer.py
│       └── command.py
├── tests/                     # Unit-тесты для каждого паттерна
│   ├── test_creational.py
│   ├── test_structural.py
│   └── test_behavioral.py
├── docs/                      # Документация
│   ├── CREATIONAL.md
│   ├── STRUCTURAL.md
│   └── BEHAVIORAL.md
├── README.md                  # Этот файл
├── setup.py
├── pyproject.toml
└── .gitignore
```

## Тестирование

Запуск всех тестов:

```bash
python -m pytest tests/ -v
# или
cd tests && python -m unittest discover
```

Запуск тестов отдельной категории:

```bash
python -m pytest tests/test_creational.py -v
python -m pytest tests/test_structural.py -v
python -m pytest tests/test_behavioral.py -v
```

## Документация паттернов

Подробное описание каждого паттерна находится в папке `docs/`:

- [Creational Patterns](docs/CREATIONAL.md) — Singleton, Factory, Builder
- [Structural Patterns](docs/STRUCTURAL.md) — Adapter, Decorator, Facade
- [Behavioral Patterns](docs/BEHAVIORAL.md) — Strategy, Observer, Command

## Примеры использования отдельных паттернов

Каждый паттерн в папке `patterns/` можно использовать отдельно:

```python
# Singleton
from patterns.creational import Singleton
config = Singleton(value=42)

# Factory
from patterns.creational import AnimalFactory
dog = AnimalFactory.create('dog')

# Builder
from patterns.creational import CarBuilder
car = CarBuilder().add_engine('V8').add_wheels(4).build()

# Strategy
from patterns.behavioral import Sorter, PythonSort
sorter = Sorter(PythonSort())
result = sorter.perform([3, 1, 2])

# Observer
from patterns.behavioral import Subject, PrintObserver
subject = Subject()
subject.attach(PrintObserver())
subject.notify('event')
```

## Интеграция в проекты Monolith/Microservice

Все классы и функции готовы к использованию в основном приложении:

```python
from patterns.creational import Singleton
from patterns.behavioral import Strategy, Sorter

class AnalysisConfig(Singleton):
    def __init__(self):
        self.quality = 'high'
        self.format = 'GeoTIFF'

class CustomStrategy(Strategy):
    def sort(self, data):
        return sorted(data, reverse=True)

config = AnalysisConfig()
sorter = Sorter(CustomStrategy())
```

## Разработка

Все компоненты следуют стандартам:

- Используют `logging` для вывода
- Имеют type hints и docstrings
- Покрыты unit-тестами
- Экспортируют публичные интерфейсы через `__init__.py`

## Лицензия

MIT
