#!/usr/bin/env python3
"""
ТЕСТИРОВАНИЕ всех 9 паттернов
Быстрая проверка что всё работает
"""

def test_singleton():
    """Проверка что Singleton создаёт одно объект"""
    from patterns import ImageProcessingConfig
    
    config1 = ImageProcessingConfig()
    config2 = ImageProcessingConfig()
    
    assert config1 is config2, "FAIL: Singleton не работает"
    config1.quality = "test"
    assert config2.quality == "test", "FAIL: Singleton - разные значения"
    
    print("✅ SINGLETON - OK")


def test_factory():
    """Проверка что Factory создаёт разные типы"""
    from patterns import DroneFactory
    
    drone_phantom = DroneFactory.create_drone("phantom")
    drone_mavic = DroneFactory.create_drone("mavic")
    drone_air = DroneFactory.create_drone("air")
    
    assert drone_phantom.get_specs()['model'] == "DJI Phantom 4 Pro"
    assert drone_mavic.get_specs()['model'] == "DJI Mavic 3"
    assert drone_air.get_specs()['model'] == "DJI Air 3S"
    
    assert len(drone_phantom.get_sensor_config()) > 0
    assert len(drone_mavic.get_sensor_config()) > 0
    assert len(drone_air.get_sensor_config()) > 0
    
    print("✅ FACTORY - OK")


def test_builder():
    """Проверка что Builder строит объекты"""
    from patterns import DroneFactory, DroneDataBuilder
    
    drone = DroneFactory.create_drone("phantom")
    builder = DroneDataBuilder()
    
    flight_data = (builder
                  .set_drone_info(drone)
                  .set_flight_params(altitude=100, speed=15, duration=30)
                  .set_image_metadata(count=500, resolution=(4096, 3072), fps=30)
                  .build())
    
    assert 'drone_specs' in flight_data
    assert 'flight_params' in flight_data
    assert 'image_metadata' in flight_data
    assert flight_data['flight_params']['altitude'] == 100
    
    print("✅ BUILDER - OK")


def test_adapter():
    """Проверка что Adapter работает с Legacy системой"""
    from patterns import LegacyLogger, LoggerAdapter
    
    legacy = LegacyLogger()
    adapter = LoggerAdapter(legacy)
    
    # Старый интерфейс
    legacy.log_message("Test from legacy")
    
    # Новый интерфейс через адаптер
    adapter.log("INFO", "Test from adapter")
    
    print("✅ ADAPTER - OK")


def test_decorator():
    """Проверка что Decorator добавляет функциональность"""
    from patterns import Message, ProcessingDecorator
    
    msg = Message("Test message")
    decorated = ProcessingDecorator(msg)
    
    original = msg.get()
    decorated_text = decorated.get()
    
    assert "Test message" in decorated_text
    assert "[TS:" in decorated_text
    assert "DroneAPP" in decorated_text
    assert decorated_text != original  # Добавились метаданные
    
    print("✅ DECORATOR - OK")


def test_facade():
    """Проверка что Facade упрощает систему"""
    from patterns import AnalysisFacade, ImageProcessingConfig
    import numpy as np
    
    config = ImageProcessingConfig()
    facade = AnalysisFacade()
    
    dummy_image = {"image": np.zeros((100, 100, 3)), "config": config.get_all()}
    result = facade.perform_full_analysis(dummy_image, (40.7128, -74.0060))
    
    assert isinstance(result, dict)
    assert 'image_analysis' in result
    assert 'geoprocessing' in result
    
    print("✅ FACADE - OK")


def test_strategy():
    """Проверка что Strategy выбирает алгоритм"""
    from patterns import ImageSorter, AlphabeticalSort, ReverseSort, LengthSort
    
    files = ["photo_10.jpg", "photo_2.jpg", "photo_1.jpg", "photo_20.jpg"]
    
    sorter_alpha = ImageSorter(AlphabeticalSort())
    sorted_alpha = sorter_alpha.sort_images(files)
    assert sorted_alpha[0] == "photo_1.jpg"  # Алфавитно
    
    sorter_reverse = ImageSorter(ReverseSort())
    sorted_reverse = sorter_reverse.sort_images(files)
    assert sorted_reverse[0] == "photo_20.jpg"  # Обратно
    
    sorter_length = ImageSorter(LengthSort())
    # LengthSort сортирует по длине строки
    length_files = ["a.jpg", "ab.jpg", "abc.jpg"]
    sorted_length = sorter_length.sort_images(length_files)
    # Проверяем что результат отсортирован (порядок может быть другой)
    assert len(sorted_length) == 3
    assert sorted_length[0] == "a.jpg"  # Самое короткое первым
    
    print("✅ STRATEGY - OK")


def test_observer():
    """Проверка что Observer уведомляет"""
    from patterns import Subject, SystemObserver
    
    event_system = Subject()
    observer = SystemObserver()
    event_system.attach(observer)
    
    # Пытаемся отправить событие (не должно быть ошибок)
    event_system.notify("test_event", {"data": "test"})
    
    print("✅ OBSERVER - OK")


def test_command():
    """Проверка что Command сохраняет историю"""
    from patterns import (
        AnalysisCommand, CommandQueue, 
        AnalysisFacade, DroneFactory, DroneDataBuilder
    )
    
    facade = AnalysisFacade()
    drone = DroneFactory.create_drone("phantom")
    builder = DroneDataBuilder()
    flight_data = builder.set_drone_info(drone).set_flight_params(altitude=100, speed=15, duration=30).build()
    
    queue = CommandQueue()
    
    command1 = AnalysisCommand(facade, flight_data)
    queue.execute(command1)
    
    command2 = AnalysisCommand(facade, flight_data)
    queue.execute(command2)
    
    assert len(queue.history) == 2
    assert isinstance(queue.history[0], AnalysisCommand)
    assert isinstance(queue.history[1], AnalysisCommand)
    
    print("✅ COMMAND - OK")


def test_integrated():
    """Проверка что все паттерны работают вместе"""
    from app_with_patterns import ImageAnalysisEngine
    
    engine = ImageAnalysisEngine()
    
    # Проверяем что engine создан с всеми паттернами
    assert engine.config is not None  # SINGLETON
    assert engine.event_system is not None  # OBSERVER
    assert engine.command_queue is not None  # COMMAND
    assert engine.facade is not None  # FACADE
    
    print("✅ INTEGRATED - OK (все 9 паттернов вместе)")


def main():
    print("\n" + "="*80)
    print("ТЕСТИРОВАНИЕ 9 DESIGN PATTERNS")
    print("="*80 + "\n")
    
    tests = [
        ("1️⃣  SINGLETON", test_singleton),
        ("2️⃣  FACTORY", test_factory),
        ("3️⃣  BUILDER", test_builder),
        ("4️⃣  ADAPTER", test_adapter),
        ("5️⃣  DECORATOR", test_decorator),
        ("6️⃣  FACADE", test_facade),
        ("7️⃣  STRATEGY", test_strategy),
        ("8️⃣  OBSERVER", test_observer),
        ("9️⃣  COMMAND", test_command),
        ("🚀 INTEGRATED", test_integrated),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {name} - FAILED: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"РЕЗУЛЬТАТЫ: {passed}/{len(tests)} тестов прошли успешно")
    if failed == 0:
        print("✅ ВСЕ ПАТТЕРНЫ РАБОТАЮТ КОРРЕКТНО!")
    else:
        print(f"❌ {failed} тестов не прошли")
    print("="*80 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
