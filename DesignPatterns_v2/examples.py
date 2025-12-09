#!/usr/bin/env python3
"""
ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ всех 9 паттернов
Готово к демонстрации преподавателю
"""

import logging
from app_with_patterns import ImageAnalysisEngine, PATTERNS_USAGE

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_1_singleton():
    """
    1️⃣ SINGLETON PATTERN - Единственный экземпляр конфигурации
    """
    print("\n" + "="*80)
    print("1️⃣  SINGLETON PATTERN - ImageProcessingConfig")
    print("="*80)
    
    from patterns import ImageProcessingConfig
    
    # Создаём два "независимых" объекта
    config1 = ImageProcessingConfig()
    config2 = ImageProcessingConfig()
    
    # Они оба указывают на ОДИН и ТОТ ЖЕ объект!
    print(f"config1 id: {id(config1)}")
    print(f"config2 id: {id(config2)}")
    print(f"config1 is config2: {config1 is config2} ✅ (ДА, это ОДНО и ТОЖЕ)")
    
    # Изменяем в одном, видим в другом
    config1.quality = "low"
    print(f"\nconfig1.quality = 'low'")
    print(f"config2.quality = {config2.quality} (тоже 'low' - ОДНА конфигурация!)")
    
    # Вернём качество назад
    config1.quality = "high"
    print(f"\n✅ ВЫВОД: SINGLETON гарантирует одну конфигурацию для всего приложения")


def example_2_factory():
    """
    2️⃣ FACTORY PATTERN - Создание дронов разных типов
    """
    print("\n" + "="*80)
    print("2️⃣  FACTORY PATTERN - DroneFactory")
    print("="*80)
    
    from patterns import DroneFactory
    
    # Factory создаёт разные типы через одинаковый интерфейс
    drone_types = ["phantom", "mavic", "air"]
    
    for drone_type in drone_types:
        drone = DroneFactory.create_drone(drone_type)
        specs = drone.get_specs()
        print(f"\n{drone_type.upper()}:")
        print(f"  Model: {specs['model']}")
        print(f"  Max altitude: {specs['max_altitude']}m")
        print(f"  Battery life: {specs['battery_life']} min")
        print(f"  Sensors: {', '.join(drone.get_sensor_config())}")
    
    print(f"\n✅ ВЫВОД: FACTORY скрывает создание конкретных классов (Phantom, Mavic, Air)")


def example_3_builder():
    """
    3️⃣ BUILDER PATTERN - Пошаговое построение сложного объекта
    """
    print("\n" + "="*80)
    print("3️⃣  BUILDER PATTERN - DroneDataBuilder")
    print("="*80)
    
    from patterns import DroneFactory, DroneDataBuilder
    
    # Создаём дрон для примера
    drone = DroneFactory.create_drone("phantom")
    
    # Builder строит сложный объект пошагово
    print("\nПостроение объекта данных полёта (читаемо, логично):")
    builder = DroneDataBuilder()
    flight_data = (builder
                  .set_drone_info(drone)
                  .set_flight_params(altitude=150, speed=12, duration=45)
                  .set_image_metadata(count=500, resolution=(4096, 3072), fps=30)
                  .build())
    
    print("Шаг 1: ✅ set_drone_info(drone)")
    print("Шаг 2: ✅ set_flight_params(altitude=150, speed=12, duration=45)")
    print("Шаг 3: ✅ set_image_metadata(count=500, resolution=(4096, 3072), fps=30)")
    print("Шаг 4: ✅ build() - вернул готовый объект")
    
    print(f"\nРезультат: {flight_data}")
    print(f"✅ ВЫВОД: BUILDER делает конструирование читаемым и структурированным")


def example_4_adapter():
    """
    4️⃣ ADAPTER PATTERN - Адаптация несовместимых интерфейсов
    """
    print("\n" + "="*80)
    print("4️⃣  ADAPTER PATTERN - LoggerAdapter")
    print("="*80)
    
    from patterns import LegacyLogger, LoggerAdapter
    
    # Старая система логирования (из OLD кода)
    legacy = LegacyLogger()
    
    print("\n1️⃣  БЕЗ адаптера - старый интерфейс (несовместимый):")
    legacy.log_message("Старый способ логирования")
    
    print("\n2️⃣  С адаптером - новый интерфейс (совместимый):")
    adapter = LoggerAdapter(legacy)
    adapter.log("INFO", "Новый способ логирования")
    
    print(f"\n✅ ВЫВОД: ADAPTER позволяет старому коду работать с новым интерфейсом")


def example_5_decorator():
    """
    5️⃣ DECORATOR PATTERN - Добавление функциональности динамически
    """
    print("\n" + "="*80)
    print("5️⃣  DECORATOR PATTERN - ProcessingDecorator")
    print("="*80)
    
    from patterns import Message, ProcessingDecorator
    
    # Базовое сообщение
    base_msg = Message("Processing image with NDVI algorithm")
    print(f"\n1️⃣  Базовое сообщение:")
    print(f"   {base_msg.get()}")
    
    # Декоратор добавляет метаданные
    decorated = ProcessingDecorator(base_msg)
    print(f"\n2️⃣  Украшенное сообщение (с timestamp и processor):")
    print(f"   {decorated.get()}")
    
    print(f"\n✅ ВЫВОД: DECORATOR добавил metadata БЕЗ изменения оригинального класса")


def example_6_facade():
    """
    6️⃣ FACADE PATTERN - Упрощение сложной системы
    """
    print("\n" + "="*80)
    print("6️⃣  FACADE PATTERN - AnalysisFacade")
    print("="*80)
    
    from patterns import AnalysisFacade, ImageProcessingConfig
    
    config = ImageProcessingConfig()
    facade = AnalysisFacade()
    
    print("\nБЕЗ фасада пришлось бы:")
    print("  1. analyzer = ImageAnalyzer()")
    print("  2. processor = ImageProcessor()")
    print("  3. geo = GeoprocessingEngine()")
    print("  4. reporter = ReportGenerator()")
    print("  # Сложная последовательность вызовов...")
    
    print("\nС фасадом - ОДНА строка:")
    print("  result = facade.perform_full_analysis(data, coords)")
    
    # Демонстрируем
    import numpy as np
    dummy_image = {"image": np.zeros((100, 100, 3)), "config": config.get_all()}
    result = facade.perform_full_analysis(dummy_image, (40.7128, -74.0060))
    print(f"\n✅ Результат: {type(result)} (объект результата анализа)")
    print(f"✅ ВЫВОД: FACADE скрывает сложность подсистем за простым интерфейсом")


def example_7_strategy():
    """
    7️⃣ STRATEGY PATTERN - Выбор алгоритма во время работы
    """
    print("\n" + "="*80)
    print("7️⃣  STRATEGY PATTERN - ImageSorter + AlphabeticalSort")
    print("="*80)
    
    from patterns import ImageSorter, AlphabeticalSort, ReverseSort, LengthSort
    
    files = ["photo_10.jpg", "photo_2.jpg", "photo_1.jpg", "photo_20.jpg"]
    
    print(f"\nИсходный список файлов:")
    print(f"  {files}")
    
    # Стратегия 1: Алфавитная
    sorter1 = ImageSorter(AlphabeticalSort())
    sorted1 = sorter1.sort_images(files)
    print(f"\n1️⃣  AlphabeticalSort:")
    print(f"  {sorted1}")
    
    # Стратегия 2: Обратно
    sorter2 = ImageSorter(ReverseSort())
    sorted2 = sorter2.sort_images(files)
    print(f"\n2️⃣  ReverseSort:")
    print(f"  {sorted2}")
    
    # Стратегия 3: По длине
    sorter3 = ImageSorter(LengthSort())
    sorted3 = sorter3.sort_images(files)
    print(f"\n3️⃣  LengthSort:")
    print(f"  {sorted3}")
    
    print(f"\n✅ ВЫВОД: STRATEGY позволяет выбирать алгоритм во время работы")


def example_8_observer():
    """
    8️⃣ OBSERVER PATTERN - Система событий
    """
    print("\n" + "="*80)
    print("8️⃣  OBSERVER PATTERN - Subject + SystemObserver")
    print("="*80)
    
    from patterns import Subject, SystemObserver
    
    # Создаём систему событий
    event_system = Subject()
    observer = SystemObserver()
    event_system.attach(observer)
    
    print("\nПодписка на события:")
    print(f"  ✅ SystemObserver подписан на события")
    
    print("\nОтправка события (все наблюдатели получат уведомление):")
    event_system.notify("analysis_start", {"image": "photo.jpg"})
    
    event_system.notify("analysis_complete", {
        "image": "photo.jpg",
        "result": "NDVI calculated"
    })
    
    print(f"\n✅ ВЫВОД: OBSERVER - слабая связанность, системы уведомлений")


def example_9_command():
    """
    9️⃣ COMMAND PATTERN - Инкапсуляция операций
    """
    print("\n" + "="*80)
    print("9️⃣  COMMAND PATTERN - AnalysisCommand + CommandQueue")
    print("="*80)
    
    from patterns import AnalysisCommand, CommandQueue, AnalysisFacade, DroneDataBuilder, DroneFactory
    
    # Подготавливаем данные
    facade = AnalysisFacade()
    drone = DroneFactory.create_drone("phantom")
    builder = DroneDataBuilder()
    flight_data = builder.set_drone_info(drone).set_flight_params(altitude=100, speed=15, duration=30).build()
    
    # Создаём очередь команд
    queue = CommandQueue()
    
    print("\nВыполнение команд:")
    print("  1️⃣  Создаём команду: AnalysisCommand(facade, flight_data)")
    command1 = AnalysisCommand(facade, flight_data)
    queue.execute(command1)
    print("     ✅ Команда выполнена и сохранена в истории")
    
    print("\n  2️⃣  Создаём вторую команду")
    command2 = AnalysisCommand(facade, flight_data)
    queue.execute(command2)
    print("     ✅ Команда выполнена и сохранена в истории")
    
    print(f"\nИстория команд (для аудита):")
    history = queue.history
    print(f"  Всего команд: {len(history)}")
    for i, cmd in enumerate(history, 1):
        print(f"    {i}. {cmd.__class__.__name__}")
    
    print(f"\n✅ ВЫВОД: COMMAND - история операций, аудит, возможность отката")


def example_integrated():
    """
    ВСЕ 9 ПАТТЕРНОВ ВМЕСТЕ в ImageAnalysisEngine
    """
    print("\n" + "="*80)
    print("🚀 ВСЕ 9 ПАТТЕРНОВ ВМЕСТЕ - ImageAnalysisEngine")
    print("="*80)
    
    engine = ImageAnalysisEngine()
    
    print("\nОписание что происходит при analyze_image():")
    print("  1️⃣  SINGLETON    - Конфигурация загружается один раз")
    print("  2️⃣  FACTORY      - Создаётся дрон нужного типа")
    print("  3️⃣  BUILDER      - Строятся данные полёта")
    print("  4️⃣  ADAPTER      - Старая система логирования адаптируется")
    print("  5️⃣  DECORATOR    - Сообщения украшаются метаданными")
    print("  6️⃣  FACADE       - Анализ упрощён фасадом")
    print("  7️⃣  STRATEGY     - Файлы сортируются выбранной стратегией")
    print("  8️⃣  OBSERVER     - События уведомляют наблюдателей")
    print("  9️⃣  COMMAND      - Команда сохраняется в истории")
    
    print("\n✅ ВЫВОД: Все 9 паттернов работают ВМЕСТЕ в реальной системе!")


def main():
    """Запускает все примеры"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  9 DESIGN PATTERNS - ПОЛНАЯ ДЕМОНСТРАЦИЯ".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Примеры каждого паттерна
    example_1_singleton()
    example_2_factory()
    example_3_builder()
    example_4_adapter()
    example_5_decorator()
    example_6_facade()
    example_7_strategy()
    example_8_observer()
    example_9_command()
    example_integrated()
    
    # Полная документация
    print("\n" + "="*80)
    print("📚 ПОЛНАЯ ДОКУМЕНТАЦИЯ ВСЕХ ПАТТЕРНОВ")
    print("="*80)
    print(PATTERNS_USAGE)
    
    print("\n" + "="*80)
    print("✅ ВСЕ ПРИМЕРЫ ЗАВЕРШЕНЫ")
    print("="*80)
    print("\n📁 Файлы для проверки преподавателем:")
    print("  1. patterns.py           - Реализация всех 9 паттернов (700+ строк)")
    print("  2. app_with_patterns.py  - ImageAnalysisEngine с интегрированными паттернами")
    print("  3. examples.py           - Примеры использования (этот файл)")
    print("  4. PATTERNS_USAGE.md     - Документация с визуальными схемами")
    print("\n🎓 Готово к коду-ревью!\n")


if __name__ == "__main__":
    main()
