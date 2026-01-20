# Creational Patterns

Паттерны, отвечающие за создание объектов.

## Singleton

Гарантирует, что класс имеет одиночный экземпляр и предоставляет глобальную точку доступа к этому экземпляру.

**Использование**: Конфигурационные объекты, логгеры, пулы подключений.

```python
from patterns.creational import Singleton
s1 = Singleton(value=10)
s2 = Singleton(value=20)
assert s1 is s2  # Один и тот же объект
```

## Factory

Инкапсулирует логику создания объектов в отдельный класс или метод.

**Использование**: Создание объектов на основе параметров, полиморфизм.

```python
from patterns.creational import AnimalFactory
dog = AnimalFactory.create('dog')
print(dog.speak())  # 'woof'
```

## Builder

Разделяет конструирование сложного объекта и его представление.

**Использование**: Создание объектов со множеством параметров конфигурации.

```python
from patterns.creational import CarBuilder
car = CarBuilder().add_engine('V8').add_wheels(4).build()
```
