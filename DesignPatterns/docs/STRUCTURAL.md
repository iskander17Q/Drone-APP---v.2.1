# Structural Patterns

Паттерны, отвечающие за скомпонованность объектов и классов.

## Adapter

Преобразует интерфейс одного класса в интерфейс другого, который ожидает клиент.

**Использование**: Интеграция несовместимых интерфейсов, обёртывание старого кода.

```python
from patterns.structural import LoggerAdapter, OldLogger
old = OldLogger()
adapter = LoggerAdapter(old)
adapter.log('message')
```

## Decorator

Динамически добавляет новые функции объекту, оборачивая его.

**Использование**: Расширение функциональности без изменения классов, кеширование.

```python
from patterns.structural import make_bold, greet
result = greet('World')  # <b>Hello, World</b>
```

## Facade

Предоставляет единый интерфейс для набора интерфейсов в подсистеме.

**Использование**: Упрощение взаимодействия с комплексными системами.

```python
from patterns.structural import Facade
facade = Facade()
print(facade.do_work())
```
