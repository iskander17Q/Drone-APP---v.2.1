"""
Design Patterns Integration Module for Drone Image Analysis System
Integrates 9 design patterns into the existing application
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import threading

logger = logging.getLogger(__name__)


# ============================================================================
# CREATIONAL PATTERNS
# ============================================================================

# 1. SINGLETON - Image Processing Configuration
class ImageProcessingConfig:
    """Singleton pattern - manages application configuration"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.quality = "high"
        self.format = "TIFF"
        self.compression = "lzw"
        self.color_space = "RGB"
        self.threshold_ndvi = 0.5
        self.auto_enhance = True
        self._initialized = True
        logger.info("ImageProcessingConfig initialized (Singleton)")
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        logger.info(f"Configuration updated: {kwargs}")
    
    def get_all(self) -> Dict[str, Any]:
        return {
            'quality': self.quality,
            'format': self.format,
            'compression': self.compression,
            'color_space': self.color_space,
            'threshold_ndvi': self.threshold_ndvi,
            'auto_enhance': self.auto_enhance
        }


# 2. FACTORY - Drone Object Creation
class Drone(ABC):
    """Abstract drone class"""
    @abstractmethod
    def get_specs(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_sensor_config(self) -> List[str]:
        pass


class PhantomDrone(Drone):
    def get_specs(self):
        return {
            'model': 'DJI Phantom 4 Pro',
            'max_altitude': 6000,
            'max_speed': 20,
            'battery_life': 28,
            'weight': 1375
        }
    
    def get_sensor_config(self):
        return ['RGB', 'Thermal', 'NIR']


class MavicDrone(Drone):
    def get_specs(self):
        return {
            'model': 'DJI Mavic 3',
            'max_altitude': 6000,
            'max_speed': 19,
            'battery_life': 46,
            'weight': 895
        }
    
    def get_sensor_config(self):
        return ['RGB', 'Thermal', 'Tele']


class AirDrone(Drone):
    def get_specs(self):
        return {
            'model': 'DJI Air 3S',
            'max_altitude': 7000,
            'max_speed': 20,
            'battery_life': 46,
            'weight': 738
        }
    
    def get_sensor_config(self):
        return ['RGB', 'Thermal']


class DroneFactory:
    """Factory pattern - creates drone instances"""
    
    _drone_classes = {
        'phantom': PhantomDrone,
        'mavic': MavicDrone,
        'air': AirDrone
    }
    
    @classmethod
    def create_drone(cls, drone_type: str) -> Drone:
        drone_class = cls._drone_classes.get(drone_type.lower())
        if drone_class is None:
            raise ValueError(f"Unknown drone type: {drone_type}")
        drone = drone_class()
        logger.info(f"Drone created: {drone_class.__name__} (Factory)")
        return drone


# 3. BUILDER - Complex Object Construction
class DroneDataBuilder:
    """Builder pattern - constructs complex drone analysis data"""
    
    def __init__(self):
        self.data = {}
    
    def set_drone_info(self, drone: Drone):
        self.data['drone_specs'] = drone.get_specs()
        self.data['sensors'] = drone.get_sensor_config()
        return self
    
    def set_flight_params(self, altitude: int, speed: int, duration: int):
        self.data['flight_params'] = {
            'altitude': altitude,
            'speed': speed,
            'duration': duration
        }
        return self
    
    def set_image_metadata(self, count: int, resolution: tuple, fps: int):
        self.data['image_metadata'] = {
            'count': count,
            'resolution': resolution,
            'fps': fps,
            'timestamp': datetime.now().isoformat()
        }
        return self
    
    def build(self) -> Dict[str, Any]:
        if not self.data:
            raise ValueError("No data set for builder")
        logger.info("DroneData built (Builder)")
        return self.data.copy()


# ============================================================================
# STRUCTURAL PATTERNS
# ============================================================================

# 4. ADAPTER - Legacy Logger Integration
class LegacyLogger:
    """Legacy logging system"""
    def log_message(self, msg: str):
        print(f"[OLD_LOG] {msg}")


class LoggerAdapter:
    """Adapter pattern - adapts legacy logger to new system"""
    
    def __init__(self, legacy_logger: LegacyLogger):
        self.legacy_logger = legacy_logger
    
    def log(self, level: str, message: str):
        self.legacy_logger.log_message(f"[{level}] {message}")
        logger.log(getattr(logging, level), f"[Adapted] {message}")


# 5. DECORATOR - Add Metadata to Messages
class Message:
    def __init__(self, content: str):
        self.content = content
    
    def get(self) -> str:
        return self.content


class ProcessingDecorator(Message):
    """Decorator pattern - adds processing metadata"""
    
    def __init__(self, message: Message):
        self.message = message
        self.metadata = {
            'timestamp': datetime.now().isoformat(),
            'processor': 'DroneAPP'
        }
    
    def get(self) -> str:
        meta_str = f" [TS: {self.metadata['timestamp']}, By: {self.metadata['processor']}]"
        return self.message.get() + meta_str


# 6. FACADE - Simplify Complex Subsystems
class ImageAnalysisSubsystem:
    def analyze(self, image_data: Dict) -> Dict:
        return {'indices': ['NDVI', 'GNDVI'], 'quality': 'high'}


class GeoprocessingSubsystem:
    def process(self, coords: tuple) -> Dict:
        return {'georeferenced': True, 'projection': 'WGS84'}


class ReportingSubsystem:
    def generate(self, analysis: Dict) -> str:
        return f"Report: {len(analysis)} items"


class AnalysisFacade:
    """Facade pattern - simplifies complex subsystems"""
    
    def __init__(self):
        self.image_analysis = ImageAnalysisSubsystem()
        self.geoprocessing = GeoprocessingSubsystem()
        self.reporting = ReportingSubsystem()
    
    def perform_full_analysis(self, image_data: Dict, coords: tuple) -> Dict:
        analysis = self.image_analysis.analyze(image_data)
        geo_result = self.geoprocessing.process(coords)
        report = self.reporting.generate(analysis)
        
        logger.info("Full analysis performed (Facade)")
        return {
            'image_analysis': analysis,
            'geoprocessing': geo_result,
            'report': report
        }


# ============================================================================
# BEHAVIORAL PATTERNS
# ============================================================================

# 7. STRATEGY - Algorithm Selection
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, items: List[str]) -> List[str]:
        pass


class AlphabeticalSort(SortStrategy):
    def sort(self, items: List[str]) -> List[str]:
        return sorted(items)


class ReverseSort(SortStrategy):
    def sort(self, items: List[str]) -> List[str]:
        return sorted(items, reverse=True)


class LengthSort(SortStrategy):
    def sort(self, items: List[str]) -> List[str]:
        return sorted(items, key=len)


class ImageSorter:
    """Strategy pattern - selects sorting algorithm at runtime"""
    
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def sort_images(self, image_list: List[str]) -> List[str]:
        result = self.strategy.sort(image_list)
        logger.info(f"Images sorted using {self.strategy.__class__.__name__} (Strategy)")
        return result


# 8. OBSERVER - Event System
class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: Dict):
        pass


class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event: str, data: Dict):
        for observer in self._observers:
            observer.update(event, data)


class SystemObserver(Observer):
    """Observer pattern - monitors system events"""
    
    def update(self, event: str, data: Dict):
        logger.info(f"System Event: {event} | Data: {data}")


class AnalysisObserver(Observer):
    def update(self, event: str, data: Dict):
        logger.info(f"Analysis Event: {event}")


# 9. COMMAND - Encapsulate Operations
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


class AnalysisCommand(Command):
    def __init__(self, analyzer: 'AnalysisFacade', image_data: Dict):
        self.analyzer = analyzer
        self.image_data = image_data
        self.result = None
    
    def execute(self):
        self.result = self.analyzer.perform_full_analysis(self.image_data, (0, 0))
        logger.info("AnalysisCommand executed (Command)")
        return self.result
    
    def undo(self):
        self.result = None
        logger.info("AnalysisCommand undone")


class CommandQueue:
    """Command pattern - queues and executes commands"""
    
    def __init__(self):
        self.history: List[Command] = []
    
    def execute(self, command: Command):
        result = command.execute()
        self.history.append(command)
        return result
    
    def undo_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            logger.info("Last command undone")


# ============================================================================
# INTEGRATED APPLICATION
# ============================================================================

class DroneAnalysisApplication:
    """Main application integrating all 9 patterns"""
    
    def __init__(self):
        # Singleton
        self.config = ImageProcessingConfig()
        
        # Observer
        self.subject = Subject()
        self.subject.attach(SystemObserver())
        
        # Facade
        self.facade = AnalysisFacade()
        
        # Command
        self.command_queue = CommandQueue()
        
        logger.info("DroneAnalysisApplication initialized with 9 patterns")
    
    def analyze_images(self, drone_type: str, image_count: int) -> Dict[str, Any]:
        """Execute complete analysis pipeline using all patterns"""
        
        # Factory pattern - create drone
        drone = DroneFactory.create_drone(drone_type)
        self.subject.notify("drone_selected", {"type": drone_type})
        
        # Builder pattern - construct complex data
        builder = DroneDataBuilder()
        data = (builder
                .set_drone_info(drone)
                .set_flight_params(100, 15, 30)
                .set_image_metadata(image_count, (4096, 3072), 30)
                .build())
        
        # Decorator pattern - add metadata to message
        msg = Message(f"Analyzing {image_count} images from {drone_type}")
        decorated_msg = ProcessingDecorator(msg)
        logger.info(decorated_msg.get())
        
        # Strategy pattern - sort images
        sorter = ImageSorter(AlphabeticalSort())
        images = [f"image_{i}.jpg" for i in range(image_count)]
        sorted_images = sorter.sort_images(images)
        
        # Command pattern - execute analysis
        command = AnalysisCommand(self.facade, data)
        analysis_result = self.command_queue.execute(command)
        
        # Adapter pattern - log with legacy system
        legacy_logger = LegacyLogger()
        adapter = LoggerAdapter(legacy_logger)
        adapter.log("INFO", f"Analysis complete: {len(sorted_images)} images processed")
        
        self.subject.notify("analysis_complete", {"status": "success"})
        
        return {
            "drone_specs": drone.get_specs(),
            "sensors": drone.get_sensor_config(),
            "images_processed": len(sorted_images),
            "image_list": sorted_images,
            "analysis_data": analysis_result,
            "configuration": self.config.get_all()
        }


def demonstrate_patterns():
    """Demonstrate all 9 patterns"""
    logger.info("=" * 70)
    logger.info("DRONE IMAGE ANALYSIS SYSTEM - 9 DESIGN PATTERNS DEMONSTRATION")
    logger.info("=" * 70)
    
    app = DroneAnalysisApplication()
    
    # Test with different drones
    drones = [("phantom", 5), ("mavic", 3), ("air", 4)]
    
    for drone_type, count in drones:
        logger.info(f"\n>>> Analyzing with {drone_type.upper()}")
        result = app.analyze_images(drone_type, count)
        logger.info(f"Result: {result['drone_specs']['model']} with {result['images_processed']} images")
    
    logger.info("\n" + "=" * 70)
    logger.info("DEMONSTRATION COMPLETE")
    logger.info("=" * 70)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    demonstrate_patterns()
