# Behavioral Patterns

Паттерны, отвечающие за общение между объектами.

## Strategy

Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.

**Использование**: Выбор алгоритма во время выполнения, сортировки, компрессия.

```python
from patterns.behavioral import Sorter, BubbleSort, PythonSort
sorter = Sorter(BubbleSort())
sorter.perform([3, 1, 2])
```

## Observer

Определяет отношение один-ко-многим между объектами таким образом, что при изменении состояния одного объекта все зависящие от него объекты уведомляются об этом.

**Использование**: Event listeners, publish-subscribe системы, реактивное программирование.

```python
from patterns.behavioral import Subject, PrintObserver
subject = Subject()
subject.attach(PrintObserver())
subject.notify('event')
```

## Command

Инкапсулирует запрос как объект, позволяя параметризовать клиентов с различными запросами.

**Использование**: Отмена/повтор операций, очереди заданий, макросы.

```python
from patterns.behavioral import Light, Switch, SwitchOnCommand
light = Light()
switch = Switch()
switch.store_and_execute(SwitchOnCommand(light))
```
