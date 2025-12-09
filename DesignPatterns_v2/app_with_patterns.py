"""
Drone Image Analysis System with Design Patterns Integration
This module integrates design patterns into the actual application logic
"""

import sys
import os
import cv2
import numpy as np
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# DESIGN PATTERNS INTEGRATION
# ============================================================================

from patterns import (
    ImageProcessingConfig,      # SINGLETON - конфиг системы
    DroneFactory,               # FACTORY - создание дронов
    DroneDataBuilder,           # BUILDER - построение данных
    AnalysisFacade,             # FACADE - упрощение анализа
    LoggerAdapter, LegacyLogger,# ADAPTER - адаптация логгеров
    ProcessingDecorator, Message,# DECORATOR - добавление метаданных
    ImageSorter, AlphabeticalSort, # STRATEGY - выбор алгоритма
    Subject, SystemObserver,    # OBSERVER - система событий
    AnalysisCommand, CommandQueue# COMMAND - инкапсуляция операций
)


class ImageAnalysisEngine:
    """
    Главный движок анализа изображений
    ДЕМОНСТРАЦИЯ ВСЕХ 9 ПАТТЕРНОВ В РЕАЛЬНОЙ ЛОГИКЕ
    """
    
    def __init__(self):
        """
        1️⃣ SINGLETON PATTERN
        Используем ImageProcessingConfig как единственный экземпляр конфигурации
        Гарантирует, что во всём приложении одна конфигурация
        """
        self.config = ImageProcessingConfig()
        logger.info("✅ Engine initialized with SINGLETON config pattern")
        
        # 8️⃣ OBSERVER PATTERN
        # Subject уведомляет всех наблюдателей о событиях
        self.event_system = Subject()
        self.event_system.attach(SystemObserver())
        
        # 9️⃣ COMMAND PATTERN
        # Сохраняем историю операций
        self.command_queue = CommandQueue()
        
        # 6️⃣ FACADE PATTERN
        # Упрощённый интерфейс для сложной системы анализа
        self.facade = AnalysisFacade()
        
        logger.info("✅ Engine initialized with all 9 patterns")
    
    def analyze_image(self, image_path: str, drone_type: str = "phantom") -> dict:
        """
        Главный метод анализа изображения с использованием паттернов
        
        ПАТТЕРНЫ ИСПОЛЬЗУЕМЫЕ:
        - SINGLETON: config управляет параметрами
        - FACTORY: создаёт объект дрона
        - BUILDER: строит данные полёта
        - FACADE: упрощает анализ
        - ADAPTER: логирует через старую систему
        - DECORATOR: добавляет метаданные
        - STRATEGY: выбирает алгоритм сортировки
        - OBSERVER: уведомляет об событиях
        - COMMAND: инкапсулирует операцию
        """
        
        try:
            logger.info(f"🔍 Starting image analysis: {image_path}")
            
            # 1️⃣ SINGLETON - используем конфиг
            self.event_system.notify("analysis_start", {"image": image_path})
            logger.info(f"Config: quality={self.config.quality}, format={self.config.format}")
            
            # 2️⃣ FACTORY - создаём дрон по типу
            drone = DroneFactory.create_drone(drone_type)
            drone_specs = drone.get_specs()
            logger.info(f"✈️ Drone created: {drone_specs['model']}")
            
            # 3️⃣ BUILDER - построили сложный объект данных
            builder = DroneDataBuilder()
            flight_data = (builder
                          .set_drone_info(drone)
                          .set_flight_params(altitude=100, speed=15, duration=30)
                          .set_image_metadata(count=1, resolution=(4096, 3072), fps=30)
                          .build())
            logger.info(f"✅ Flight data built with BUILDER pattern")
            
            # Load image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Cannot read image: {image_path}")
            
            # 5️⃣ DECORATOR - добавляем метаданные к сообщению
            msg = Message(f"Processing image with {len(drone.get_sensor_config())} sensors")
            decorated_msg = ProcessingDecorator(msg)
            logger.info(decorated_msg.get())
            
            # 6️⃣ FACADE - используем фасад для упрощения анализа
            analysis_result = self.facade.perform_full_analysis(
                {"image": image, "config": self.config.get_all()},
                (0, 0)
            )
            logger.info(f"✅ Analysis performed with FACADE pattern")
            
            # 7️⃣ STRATEGY - используем стратегию сортировки
            sorter = ImageSorter(AlphabeticalSort())
            files = [f"image_{i}.jpg" for i in range(5)]
            sorted_files = sorter.sort_images(files)
            logger.info(f"✅ Files sorted with STRATEGY pattern: {sorted_files}")
            
            # 4️⃣ ADAPTER - логируем через старую систему
            legacy_logger = LegacyLogger()
            adapter = LoggerAdapter(legacy_logger)
            adapter.log("INFO", f"Image processed: {image_path}")
            
            # 9️⃣ COMMAND - инкапсулируем операцию анализа
            command = AnalysisCommand(self.facade, flight_data)
            self.command_queue.execute(command)
            logger.info(f"✅ Command executed and stored in history")
            
            # 8️⃣ OBSERVER - уведомляем об завершении
            self.event_system.notify("analysis_complete", {
                "drone": drone_specs['model'],
                "result": analysis_result
            })
            
            result = {
                "status": "success",
                "drone": drone_specs,
                "sensors": drone.get_sensor_config(),
                "analysis": analysis_result,
                "sorted_files": sorted_files,
                "config": self.config.get_all()
            }
            
            logger.info("✅ Analysis completed successfully with all 9 patterns!")
            return result
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            self.event_system.notify("analysis_error", {"error": str(e)})
            raise
    
    def batch_analyze(self, image_paths: list, drone_type: str = "phantom") -> list:
        """
        Анализ нескольких изображений
        Демонстрирует работу паттернов с несколькими объектами
        """
        results = []
        for idx, image_path in enumerate(image_paths, 1):
            logger.info(f"Processing batch {idx}/{len(image_paths)}")
            try:
                result = self.analyze_image(image_path, drone_type)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {image_path}: {e}")
                results.append({"status": "failed", "error": str(e)})
        
        return results
    
    def get_analysis_history(self):
        """
        Возвращает историю команд (COMMAND паттерн)
        """
        return self.command_queue.history
    
    def update_config(self, **kwargs):
        """
        Обновляет конфигурацию (SINGLETON паттерн)
        """
        self.config.update(**kwargs)
        logger.info(f"✅ Configuration updated: {kwargs}")


# ============================================================================
# DOCUMENTATION - ГДЕ И ЧТО ИСПОЛЬЗУЕТСЯ
# ============================================================================

PATTERNS_USAGE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║         9 DESIGN PATTERNS - ГДЕ И КАК ОНИ ИСПОЛЬЗУЮТСЯ В ПРИЛОЖЕНИИ         ║
╚══════════════════════════════════════════════════════════════════════════════╝

1️⃣  SINGLETON - ImageProcessingConfig
    ├─ ЧТО: Управляет конфигурацией анализа (качество, формат, компрессия)
    ├─ ГДЕ: engine.config
    ├─ ЗАЧЕМ: Гарантирует единственный экземпляр конфигурации
    └─ КОД: ImageProcessingConfig._instance (потокобезопасное создание)

2️⃣  FACTORY - DroneFactory.create_drone()
    ├─ ЧТО: Создаёт объекты дронов разных типов
    ├─ ГДЕ: drone = DroneFactory.create_drone(drone_type)
    ├─ ЗАЧЕМ: Избегаем прямого создания класса, используем фабрику
    └─ КОД: Возвращает PhantomDrone, MavicDrone или AirDrone

3️⃣  BUILDER - DroneDataBuilder
    ├─ ЧТО: Строит сложные объекты данных полёта пошагово
    ├─ ГДЕ: builder.set_drone_info().set_flight_params().set_image_metadata().build()
    ├─ ЗАЧЕМ: Разбиваем конструирование на логические шаги
    └─ КОД: Возвращает полный объект данных

4️⃣  ADAPTER - LoggerAdapter
    ├─ ЧТО: Адаптирует старую логгер-систему к новой
    ├─ ГДЕ: adapter = LoggerAdapter(legacy_logger)
    ├─ ЗАЧЕМ: Интегрируем старый код без переписывания
    └─ КОД: legacy_logger.log_message() → adapter.log()

5️⃣  DECORATOR - ProcessingDecorator
    ├─ ЧТО: Добавляет метаданные (timestamp, processor) к сообщениям
    ├─ ГДЕ: decorated_msg = ProcessingDecorator(msg)
    ├─ ЗАЧЕМ: Расширяем функциональность без изменения базового класса
    └─ КОД: Добавляет [TS: 2025-12-09..., By: DroneAPP]

6️⃣  FACADE - AnalysisFacade
    ├─ ЧТО: Упрощённый интерфейс для сложной системы анализа
    ├─ ГДЕ: self.facade.perform_full_analysis()
    ├─ ЗАЧЕМ: Скрывает сложность подсистем анализа
    └─ КОД: Объединяет ImageAnalysis, Geoprocessing, Reporting

7️⃣  STRATEGY - ImageSorter + AlphabeticalSort
    ├─ ЧТО: Выбор алгоритма сортировки в runtime
    ├─ ГДЕ: sorter = ImageSorter(AlphabeticalSort())
    ├─ ЗАЧЕМ: Менять поведение без изменения кода
    └─ КОД: Можно использовать ReverseSort или LengthSort

8️⃣  OBSERVER - Subject + SystemObserver
    ├─ ЧТО: Система уведомлений о событиях
    ├─ ГДЕ: self.event_system.notify("event_name", data)
    ├─ ЗАЧЕМ: Слабая связанность между компонентами
    └─ КОД: Наблюдатели подписываются на события

9️⃣  COMMAND - AnalysisCommand + CommandQueue
    ├─ ЧТО: Инкапсуляция операции как объекта
    ├─ ГДЕ: command = AnalysisCommand(...); queue.execute(command)
    ├─ ЗАЧЕМ: История операций, возможность отмены
    └─ КОД: Сохраняет историю для аудита

╔══════════════════════════════════════════════════════════════════════════════╗
║                              ИСПОЛЬЗОВАНИЕ                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

# Создаём движок анализа
engine = ImageAnalysisEngine()

# Анализируем одно изображение
result = engine.analyze_image("photo.jpg", "phantom")

# Или пакет изображений
results = engine.batch_analyze(["img1.jpg", "img2.jpg"], "mavic")

# Обновляем конфиг (SINGLETON)
engine.update_config(quality="low", format="JPEG")

# Смотрим историю команд (COMMAND)
history = engine.get_analysis_history()
"""

if __name__ == "__main__":
    print(PATTERNS_USAGE)
    
    # Пример использования
    logger.info("Starting ImageAnalysisEngine demo...")
    engine = ImageAnalysisEngine()
    logger.info("✅ Engine created with all 9 patterns integrated!")
