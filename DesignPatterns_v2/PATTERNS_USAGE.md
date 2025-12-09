╔══════════════════════════════════════════════════════════════════════════════╗
║                    9 DESIGN PATTERNS - АНАЛИЗ ИСПОЛЬЗОВАНИЯ                   ║
║                     ГДЕ КАЖДЫЙ ПАТТЕРН РАБОТАЕТ В КОДЕ                       ║
╚══════════════════════════════════════════════════════════════════════════════╝


┌──────────────────────────────────────────────────────────────────────────────┐
│ 1️⃣  SINGLETON PATTERN - ImageProcessingConfig                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Гарантирует, что класс имеет ТОЛЬКО ОДИН экземпляр               │
│          во всём приложении                                                 │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   config1 = ImageProcessingConfig()  # Первый экземпляр                      │
│   config2 = ImageProcessingConfig()  # Второй экземпляр - ПРОБЛЕМА!         │
│   # config1.quality = "high"                                                 │
│   # config2.quality = "low"                                                  │
│   # Двойные данные, противоречие! ❌                                        │
│                                                                               │
│ РЕШЕНИЕ С SINGLETON:                                                         │
│   config1 = ImageProcessingConfig()  # Первый экземпляр                      │
│   config2 = ImageProcessingConfig()  # ТОТ ЖЕ САМЫЙ объект!                 │
│   assert config1 is config2  # True ✅                                       │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   class ImageAnalysisEngine:                                                 │
│       def __init__(self):                                                    │
│           self.config = ImageProcessingConfig()  # SINGLETON                 │
│           logger.info(f"quality={self.config.quality}")                      │
│   ```                                                                        │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Единственный источник истины для конфигурации                          │
│   ✅ Все компоненты используют одни и те же параметры                       │
│   ✅ Потокобезопасное создание                                              │
│   ✅ Ленивая инициализация (создаётся при первом обращении)                 │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 2️⃣  FACTORY PATTERN - DroneFactory                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Создаёт объекты РАЗНЫХ типов через единый интерфейс               │
│          без прямого использования new                                       │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   if drone_type == "phantom":                                                │
│       drone = PhantomDrone()  # Жёсткая связанность ❌                      │
│   elif drone_type == "mavic":                                                │
│       drone = MavicDrone()                                                   │
│   # Каждая строка - потенциальный баг при добавлении нового типа            │
│                                                                               │
│ РЕШЕНИЕ С FACTORY:                                                           │
│   drone = DroneFactory.create_drone("phantom")  # Возвращает PhantomDrone ✅ │
│   # Фабрика знает, как создать нужный тип                                   │
│   # Клиентский код не меняется при добавлении новых типов                   │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   drone = DroneFactory.create_drone(drone_type)                              │
│   drone_specs = drone.get_specs()  # Polymorphism - работает с любым типом  │
│   ```                                                                        │
│                                                                               │
│ ТИПЫ ДРОНОВ:                                                                 │
│   • PhantomDrone   - 4K камера, 20 мин полёта                               │
│   • MavicDrone     - портативный, 30 мин полёта                             │
│   • AirDrone       - 8K камера, 60 мин полёта                               │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Не нужно знать конкретные классы дронов                                │
│   ✅ Легко добавлять новые типы дронов                                       │
│   ✅ Логика выбора в одном месте (фабрика)                                  │
│   ✅ Polymorphism - все дроны имеют одинаковый интерфейс                    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 3️⃣  BUILDER PATTERN - DroneDataBuilder                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Строит СЛОЖНЫЕ объекты пошагово                                   │
│          избегая гигантских конструкторов                                    │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   # Конструктор с 20+ параметрами ❌                                        │
│   flight_data = FlightData(                                                  │
│       drone_model="Phantom 4",                                               │
│       drone_sn="SN12345",                                                    │
│       sensor_res=4096,                                                       │
│       altitude=100,                                                          │
│       speed=15,                                                              │
│       duration=30,                                                           │
│       gps_lat=40.7128,                                                       │
│       ... 15 параметров ещё                                                 │
│   )  # Нечитаемо, ошибкоопасно                                              │
│                                                                               │
│ РЕШЕНИЕ С BUILDER:                                                           │
│   flight_data = (DroneDataBuilder()                                          │
│       .set_drone_info(drone)           # Понятно                             │
│       .set_flight_params(altitude=100) # Логично структурировано              │
│       .set_image_metadata(count=1)     # Читаемо                             │
│       .build())                        # Возвращает готовый объект ✅        │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   builder = DroneDataBuilder()                                               │
│   flight_data = (builder                                                     │
│       .set_drone_info(drone)                                                 │
│       .set_flight_params(altitude=100, speed=15, duration=30)               │
│       .set_image_metadata(count=1, resolution=(4096, 3072), fps=30)         │
│       .build())                                                              │
│   ```                                                                        │
│                                                                               │
│ ПРЕИМУЩЕСТВА:                                                                │
│   ✅ Читаемый, понятный код                                                 │
│   ✅ Упорядоченное строительство                                             │
│   ✅ Проверка консистентности перед build()                                 │
│   ✅ Можно изменять данные между шагами                                      │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Разделяет конструирование от представления                              │
│   ✅ Один builder может создавать разные конфигурации                        │
│   ✅ Упрощает работу с объектами, имеющими много опций                      │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 4️⃣  ADAPTER PATTERN - LoggerAdapter                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Приводит НЕСОВМЕСТИМЫЙ интерфейс к совместимому                   │
│          позволяет работать со старым кодом как с новым                     │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   # Старая система логирования (из OLD кода)                                │
│   legacy_logger = LegacyLogger()                                             │
│   legacy_logger.log_message("INFO", "text")  # Старый интерфейс              │
│                                                                               │
│   # Новая система логирования                                               │
│   new_logger = logging.getLogger(__name__)                                   │
│   new_logger.info("text")  # Новый интерфейс                                │
│                                                                               │
│   # Как использовать оба сразу? Переписать весь код? ❌                   │
│                                                                               │
│ РЕШЕНИЕ С ADAPTER:                                                           │
│   legacy_logger = LegacyLogger()                                             │
│   adapter = LoggerAdapter(legacy_logger)  # Обёртка!                        │
│   adapter.log("INFO", "text")  # Адаптируем старый к новому ✅              │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   legacy_logger = LegacyLogger()                                             │
│   adapter = LoggerAdapter(legacy_logger)                                     │
│   adapter.log("INFO", f"Image processed: {image_path}")                      │
│   # Адаптер перенаправляет log() к legacy_logger.log_message()              │
│   ```                                                                        │
│                                                                               │
│ КАК ЭТО РАБОТАЕТ:                                                            │
│   1. Клиент вызывает adapter.log(level, message)                            │
│   2. Адаптер преобразует параметры                                           │
│   3. Адаптер вызывает legacy_logger.log_message(...)                        │
│   4. Результат одинаков для обоих интерфейсов ✅                           │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Интеграция старого кода без переписывания                              │
│   ✅ Постепенная миграция к новой системе                                    │
│   ✅ Совместимость несовместимых интерфейсов                                │
│   ✅ Сохраняет работоспособность наследованного кода                        │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 5️⃣  DECORATOR PATTERN - ProcessingDecorator                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Добавляет функциональность к объекту ДИНАМИЧЕСКИ                   │
│          оборачивает объект в "декоратор" с дополнительным поведением       │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   msg = Message("Processing")                                               │
│   # Хочу добавить timestamp? Создадим новый класс:                          │
│   msg_with_ts = MessageWithTimestamp(msg)  # Новый класс                    │
│   # Хочу добавить processor? Создадим ещё класс:                            │
│   msg_with_both = MessageWithTimestampAndProcessor(msg)  # Взрыв классов! ❌│
│                                                                               │
│ РЕШЕНИЕ С DECORATOR:                                                         │
│   msg = Message("Processing")                                               │
│   decorated = ProcessingDecorator(msg)                                       │
│   # Одна строка, и добавили timestamp и processor! ✅                       │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   msg = Message("Processing image with 4 sensors")                          │
│   decorated_msg = ProcessingDecorator(msg)                                   │
│   logger.info(decorated_msg.get())                                           │
│   # Вывод: "[TS: 2025-12-09 14:30:45.123, By: DroneAPP] Processing..."      │
│   ```                                                                        │
│                                                                               │
│ КАК ЭТО РАБОТАЕТ:                                                            │
│   1. Оригинальный объект: Message(text)                                      │
│   2. Обёртка 1: ProcessingDecorator(Message)                                 │
│      - Добавляет timestamp                                                   │
│      - Добавляет processor id                                                │
│   3. Результат: [TS: ..., By: ...] + оригинальный текст                      │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Добавляем функциональность без изменения классов                        │
│   ✅ Можно комбинировать несколько декораторов                               │
│   ✅ Гибкость: добавляем только нужное                                       │
│   ✅ Избегаем взрыва количества подклассов                                   │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 6️⃣  FACADE PATTERN - AnalysisFacade                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Предоставляет ПРОСТОЙ интерфейс к СЛОЖНОЙ системе                │
│          скрывает сложность подсистем за одной точкой входа                 │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   # Клиент должен знать про всё:                                            │
│   analyzer = ImageAnalyzer()                                                 │
│   processor = ImageProcessor()                                              │
│   geo = GeoprocessingEngine()                                                │
│   reporter = ReportGenerator()                                              │
│   # Сложная последовательность вызовов ❌                                   │
│   result = analyzer.analyze(image)                                           │
│   processed = processor.process(result)                                      │
│   geo_result = geo.process(processed)                                        │
│   report = reporter.generate(geo_result)                                     │
│                                                                               │
│ РЕШЕНИЕ С FACADE:                                                            │
│   facade = AnalysisFacade()                                                  │
│   # Одна строка! Фасад управляет всеми подсистемами ✅                      │
│   result = facade.perform_full_analysis(data, coords)                        │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   self.facade = AnalysisFacade()  # Инициализируем фасад                     │
│   analysis_result = self.facade.perform_full_analysis(                       │
│       {"image": image, "config": self.config.get_all()},                     │
│       (latitude, longitude)                                                  │
│   )                                                                          │
│   ```                                                                        │
│                                                                               │
│ ЧТО СКРЫВАЕТ ФАСАД:                                                          │
│   1. ImageAnalysis - расчёт индексов (NDVI, GNDVI, EVI)                     │
│   2. Geoprocessing - обработка GPS координат                                 │
│   3. Reporting - генерация отчётов                                           │
│   4. Orchestration - координация всех процессов                              │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Упрощаем клиентский код                                                │
│   ✅ Скрываем сложность внутренних операций                                 │
│   ✅ Слабая связанность между клиентом и подсистемами                       │
│   ✅ Изменения в подсистемах не влияют на клиента                           │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 7️⃣  STRATEGY PATTERN - ImageSorter + SortStrategy                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Инкапсулирует АЛГОРИТМ в отдельный класс                          │
│          позволяет выбирать алгоритм в RUNTIME                              │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   class ImageSorter:                                                         │
│       def sort(self, images, method):                                        │
│           if method == "alphabetical":                                       │
│               # Сортировка по алфавиту                                      │
│               return sorted(images)  # Жёсткая связанность ❌               │
│           elif method == "length":                                           │
│               return sorted(images, key=len)                                │
│           elif method == "reverse":                                          │
│               return sorted(images, reverse=True)                            │
│           # Каждый новый алгоритм - новый elif!                            │
│                                                                               │
│ РЕШЕНИЕ С STRATEGY:                                                          │
│   sorter = ImageSorter(AlphabeticalSort())  # Выбираем алгоритм             │
│   sorted_files = sorter.sort_images(files)  # Используем                     │
│   # Позже можно изменить:                                                   │
│   sorter = ImageSorter(ReverseSort())  # Другой алгоритм, тот же интерфейс ✅│
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   sorter = ImageSorter(AlphabeticalSort())                                   │
│   files = [f"image_{i}.jpg" for i in range(5)]                               │
│   sorted_files = sorter.sort_images(files)                                   │
│   ```                                                                        │
│                                                                               │
│ ДОСТУПНЫЕ СТРАТЕГИИ:                                                         │
│   • AlphabeticalSort      - A -> Z                                           │
│   • ReverseSort           - Z -> A                                           │
│   • LengthSort            - по длине имени                                   │
│   (Легко добавить новые!)                                                    │
│                                                                               │
│ КАК ЭТО РАБОТАЕТ:                                                            │
│   1. Определяем интерфейс Strategy                                           │
│   2. Создаём конкретные реализации (Alphabetical, Reverse, Length)          │
│   3. Передаём стратегию в ImageSorter                                        │
│   4. ImageSorter вызывает strategy.sort(files)                               │
│   5. Алгоритм выбирается в RUNTIME!                                          │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Избегаем множества if/elif/else                                        │
│   ✅ Легко добавлять новые алгоритмы                                         │
│   ✅ Алгоритм выбирается во время работы                                     │
│   ✅ Каждый алгоритм в отдельном классе (Single Responsibility)            │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 8️⃣  OBSERVER PATTERN - Subject + Observer                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Система УВЕДОМЛЕНИЙ - один объект (Subject) уведомляет            │
│          много объектов (Observer) об изменениях                            │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   class Analysis:                                                            │
│       def analyze(self):                                                     │
│           # Укрепили связанность - зависим от UI, логов, аналитики ❌       │
│           self.ui_listener.update("started")                                 │
│           # результат анализа...                                            │
│           self.logger_listener.log("done")                                   │
│           self.analytics_listener.track("analysis_complete")                │
│   # Если добавить нового слушателя - менять класс Analysis!                │
│                                                                               │
│ РЕШЕНИЕ С OBSERVER:                                                          │
│   event_system = Subject()                                                   │
│   event_system.attach(SystemObserver())  # Добавляем слушателей            │
│   event_system.attach(UIObserver())                                          │
│   event_system.attach(AnalyticsObserver())                                   │
│   # Теперь:                                                                  │
│   event_system.notify("analysis_start", data)  # Все получат уведомление ✅  │
│   # Добавить нового слушателя - не трогаем анализ!                         │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   self.event_system = Subject()                                              │
│   self.event_system.attach(SystemObserver())                                 │
│   # При запуске анализа:                                                    │
│   self.event_system.notify("analysis_start", {"image": path})                │
│   # При завершении:                                                         │
│   self.event_system.notify("analysis_complete", {"result": result})          │
│   # При ошибке:                                                             │
│   self.event_system.notify("analysis_error", {"error": str(e)})              │
│   ```                                                                        │
│                                                                               │
│ СОБЫТИЯ:                                                                     │
│   • analysis_start   - начало анализа                                        │
│   • analysis_complete- завершение анализа                                    │
│   • analysis_error   - ошибка при анализе                                    │
│   (Легко добавить новые события!)                                            │
│                                                                               │
│ КАК ЭТО РАБОТАЕТ:                                                            │
│   1. Observer подписывается на Subject (attach)                              │
│   2. Subject уведомляет всех Observer (notify)                               │
│   3. Каждый Observer обновляет себя (update)                                 │
│   4. Слабая связанность!                                                     │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Слабая связанность между компонентами                                  │
│   ✅ Динамическая подписка/отписка                                          │
│   ✅ One-to-many отношения                                                   │
│   ✅ Реактивная архитектура                                                  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│ 9️⃣  COMMAND PATTERN - AnalysisCommand + CommandQueue                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ЧТО ЭТО: Инкапсулирует ЗАПРОС как ОБЪЕКТ                                    │
│          позволяет хранить, передавать и откатывать операции               │
│                                                                               │
│ ПРОБЛЕМА БЕЗ ПАТТЕРНА:                                                       │
│   class AnalysisEngine:                                                      │
│       def analyze(self, data):                                               │
│           # Операция напрямую в коде ❌                                      │
│           result = do_analysis(data)                                         │
│   # Нет истории операций                                                    │
│   # Нет возможности отменить                                                │
│   # Нет логирования операций                                                │
│                                                                               │
│ РЕШЕНИЕ С COMMAND:                                                           │
│   command = AnalysisCommand(facade, data)                                    │
│   queue = CommandQueue()                                                     │
│   queue.execute(command)  # Команда исполнена и сохранена ✅                │
│   # Теперь можно:                                                            │
│   history = queue.history  # Просмотреть историю                            │
│   # В будущем: queue.undo()  # Отменить                                     │
│                                                                               │
│ ИСПОЛЬЗОВАНИЕ В КОДЕ:                                                        │
│   ```python                                                                  │
│   self.command_queue = CommandQueue()                                        │
│   # При анализе:                                                            │
│   command = AnalysisCommand(self.facade, flight_data)                        │
│   self.command_queue.execute(command)                                        │
│   # Смотрим историю:                                                        │
│   history = self.get_analysis_history()                                      │
│   ```                                                                        │
│                                                                               │
│ КАК ЭТО РАБОТАЕТ:                                                            │
│   1. Создаём объект AnalysisCommand(receiver, data)                          │
│   2. CommandQueue.execute(command)                                           │
│   3. command.execute() вызывает реальную операцию                            │
│   4. queue.history хранит историю                                            │
│   5. Позже можно вызвать undo()                                              │
│                                                                               │
│ ПРЕИМУЩЕСТВА:                                                                │
│   ✅ Операции как объекты (можно сохранять, передавать)                     │
│   ✅ История всех операций                                                   │
│   ✅ Отмена/возврат операций (в будущем)                                    │
│   ✅ Логирование и аудит                                                     │
│   ✅ Отложенное исполнение                                                   │
│   ✅ Макросы и скрипты                                                       │
│                                                                               │
│ ЗАЧЕМ НУЖЕН:                                                                 │
│   ✅ Полная история всех операций                                            │
│   ✅ Аудит для проверок преподавателя                                        │
│   ✅ Возможность отката                                                      │
│   ✅ Логирование и отладка                                                   │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                        ИНТЕГРАЦИЯ ВСЕХ ПАТТЕРНОВ                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

                    ImageAnalysisEngine
                            |
                ┌───────────┼───────────┐
                |           |           |
            SINGLETON    FACTORY     BUILDER
                |           |           |
                ▼           ▼           ▼
          Config      DroneFactory  DroneData
                        ┌───┬───┬───┐
                        │   │   │   │
                        ▼   ▼   ▼   ▼
                      Drone Types (Phantom, Mavic, Air)
                        
                ┌───────────┬───────────┐
                |           |           |
             ADAPTER    DECORATOR    FACADE
                |           |           |
                ▼           ▼           ▼
            Logger      Message      Analysis
                        Metadata      Subsystems
                        
                ┌───────────┬───────────┐
                |           |           |
             STRATEGY    OBSERVER    COMMAND
                |           |           |
                ▼           ▼           ▼
             Sorter      Events      History


╔══════════════════════════════════════════════════════════════════════════════╗
║                          ПРИМЕРЫ ВЫВОДА                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

✅ Engine initialized with SINGLETON config pattern
✅ Engine initialized with all 9 patterns
🔍 Starting image analysis: photo.jpg
Config: quality=high, format=PNG
✈️ Drone created: Phantom 4 Pro (PhantomDrone)
✅ Flight data built with BUILDER pattern
✅ ProcessingDecorator: [TS: 2025-12-09 14:30:45.123, By: DroneAPP] Processing...
✅ Analysis performed with FACADE pattern
✅ Files sorted with STRATEGY pattern: [image_1.jpg, image_2.jpg, ...]
✅ Command executed and stored in history
✅ Analysis completed successfully with all 9 patterns!
