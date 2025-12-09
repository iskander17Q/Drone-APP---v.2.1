"""
Main Design Patterns Application - integrated drone image analysis system.

Демонстрирует использование всех 9 паттернов в единой системе анализа изображений дрона.
"""
import logging
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all patterns
from patterns.creational import Singleton, AnimalFactory, CarBuilder
from patterns.structural import LoggerAdapter, OldLogger, make_bold, Facade
from patterns.behavioral import Sorter, BubbleSort, PythonSort, Subject, PrintObserver, Light, Switch, SwitchOnCommand, SwitchOffCommand


class ImageProcessingConfig(Singleton):
    """Configuration singleton - единая точка конфигурации системы."""
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.sort_strategy = PythonSort
            self.quality = 'high'
            self.drone_models = ['Phantom', 'Mavic', 'Air']
            logger.info('ImageProcessingConfig initialized')


class DroneFactory:
    """Factory для создания разных типов дронов."""
    @staticmethod
    def create_drone(drone_type):
        if drone_type == 'phantom':
            return {'model': 'Phantom', 'sensors': ['RGB', 'Thermal']}
        elif drone_type == 'mavic':
            return {'model': 'Mavic', 'sensors': ['RGB']}
        elif drone_type == 'air':
            return {'model': 'Air', 'sensors': ['RGB', 'LIDAR']}
        raise ValueError(f'Unknown drone type: {drone_type}')


class DroneDataBuilder:
    """Builder для конструирования сложных наборов данных дрона."""
    def __init__(self):
        self.data = {
            'drone': None,
            'images': [],
            'processing_params': {},
            'output_format': None
        }

    def set_drone(self, drone_type):
        self.data['drone'] = DroneFactory.create_drone(drone_type)
        return self

    def add_images(self, count):
        self.data['images'] = [f'image_{i}.jpg' for i in range(count)]
        return self

    def set_processing_params(self, **params):
        self.data['processing_params'] = params
        return self

    def set_output_format(self, fmt):
        self.data['output_format'] = fmt
        return self

    def build(self):
        return self.data


class LoggerAdapter:
    """Adapter - адаптирует старую логгер-систему к новой."""
    def __init__(self, old_logger):
        self.old_logger = old_logger

    def log_event(self, event_type, message):
        formatted = f"[{event_type}] {message}"
        self.old_logger.write(formatted)
        logger.info(formatted)


class ProcessingDecorator:
    """Decorator - добавляет функциональность к процессу обработки."""
    @staticmethod
    def add_timestamp(message):
        from datetime import datetime
        return f"[{datetime.now().isoformat()}] {message}"

    @staticmethod
    def add_priority(message, priority='NORMAL'):
        return f"[{priority}] {message}"


class AnalysisFacade:
    """Facade - упрощает взаимодействие с комплексной системой анализа."""
    def __init__(self):
        self.config = ImageProcessingConfig()
        self.logger = LoggerAdapter(OldLogger())
        self.sorter = Sorter(self.config.sort_strategy())

    def analyze_images(self, drone_type, image_count):
        logger.info('Starting analysis with Facade pattern')
        
        # Build drone data
        builder = DroneDataBuilder()
        data = builder.set_drone(drone_type).add_images(image_count).set_processing_params(quality='high', format='TIFF').set_output_format('GeoTIFF').build()
        
        self.logger.log_event('ANALYSIS_START', f"Processing {len(data['images'])} images from {data['drone']['model']}")
        
        # Sort images using strategy pattern
        sorted_images = self.sorter.perform(data['images'])
        
        self.logger.log_event('ANALYSIS_COMPLETE', f"Processed images in order: {sorted_images}")
        return data


class SystemObserver(Subject):
    """Observer - мониторит события системы."""
    def __init__(self):
        super().__init__()
        self.events = []

    def log_event(self, event):
        self.events.append(event)
        self.notify(f"System Event: {event}")


class ImageProcessingCommand:
    """Command - инкапсулирует операции обработки."""
    def __init__(self, light, operation_name):
        self.light = light
        self.operation_name = operation_name

    def execute(self):
        self.light.switch_on()
        logger.info(f"Processing: {self.operation_name}")

    def undo(self):
        self.light.switch_off()
        logger.info(f"Cancelled: {self.operation_name}")


class DroneAPP:
    """Главное приложение, интегрирующее все паттерны."""
    
    def __init__(self):
        self.facade = AnalysisFacade()
        self.observer = SystemObserver()
        self.observer.attach(PrintObserver())
        self.processing_light = Light()
        self.processing_switch = Switch()
        logger.info('DroneAPP initialized with all 9 design patterns')

    def run_analysis(self, drone_type='phantom', image_count=5):
        """Запуск анализа с использованием всех паттернов."""
        self.observer.log_event(f'Analysis started for {drone_type}')
        
        # Execute processing command
        cmd = ImageProcessingCommand(self.processing_light, f'Analyze {image_count} images')
        self.processing_switch.store_and_execute(cmd)
        
        # Run facade analysis
        result = self.facade.analyze_images(drone_type, image_count)
        
        self.observer.log_event('Analysis completed successfully')
        logger.info('Analysis result: %s', result)
        return result

    def interactive_menu(self):
        """Интерактивное меню для работы с приложением."""
        while True:
            print("\n" + "="*60)
            print("DRONE IMAGE ANALYSIS SYSTEM - Design Patterns Demo")
            print("="*60)
            print("1. Анализировать изображения (Phantom)")
            print("2. Анализировать изображения (Mavic)")
            print("3. Анализировать изображения (Air)")
            print("4. Показать конфигурацию (Singleton)")
            print("5. Показать события (Observer)")
            print("6. Выход")
            print("-"*60)
            
            choice = input("Выберите опцию (1-6): ").strip()
            
            if choice == '1':
                self.run_analysis('phantom', 5)
            elif choice == '2':
                self.run_analysis('mavic', 3)
            elif choice == '3':
                self.run_analysis('air', 4)
            elif choice == '4':
                cfg = ImageProcessingConfig()
                print(f"\nКонфигурация системы (Singleton):")
                print(f"  - Стратегия сортировки: {cfg.sort_strategy.__name__}")
                print(f"  - Качество: {cfg.quality}")
                print(f"  - Доступные дроны: {', '.join(cfg.drone_models)}")
            elif choice == '5':
                print(f"\nУтеченные события (Observer):")
                for i, event in enumerate(self.observer.events, 1):
                    print(f"  {i}. {event}")
            elif choice == '6':
                print("\nВыход из приложения.")
                break
            else:
                print("\nНеправильная опция. Попробуйте снова.")


def main():
    """Entry point приложения."""
    try:
        app = DroneAPP()
        
        if len(sys.argv) > 1 and sys.argv[1] == '--auto':
            # Автоматический режим демонстрации
            logger.info('Running in auto-demo mode')
            app.run_analysis('phantom', 5)
            app.run_analysis('mavic', 3)
        else:
            # Интерактивный режим
            app.interactive_menu()
            
    except Exception as e:
        logger.error('Application error: %s', e, exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
