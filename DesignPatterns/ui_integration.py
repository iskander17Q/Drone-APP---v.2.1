"""
UI Integration Module - connects PyQt5 UI with Design Patterns Application backend.

This module integrates the existing PyQt5 UI (main.py) with the DroneAPP backend
to demonstrate design patterns in action through a graphical interface.
"""
import sys
import logging
from PyQt5 import QtWidgets, QtCore, QtGui
from application import DroneAPP, ImageProcessingConfig

logger = logging.getLogger(__name__)


class DroneAnalysisWidget(QtWidgets.QWidget):
    """Widget that demonstrates design patterns through drone image analysis."""
    
    analysis_started = QtCore.pyqtSignal(str)
    analysis_completed = QtCore.pyqtSignal(dict)
    event_logged = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drone_app = DroneAPP()
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the UI for design patterns demonstration."""
        layout = QtWidgets.QVBoxLayout()
        
        # Title
        title = QtWidgets.QLabel("Drone Image Analysis System\n(9 Design Patterns)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        
        # Patterns info group
        patterns_group = QtWidgets.QGroupBox("Active Design Patterns")
        patterns_layout = QtWidgets.QGridLayout()
        
        patterns = [
            ("Singleton", "ImageProcessingConfig - единая конфигурация"),
            ("Factory", "DroneFactory - создание дронов"),
            ("Builder", "DroneDataBuilder - конструирование данных"),
            ("Adapter", "LoggerAdapter - адаптация логгеров"),
            ("Decorator", "ProcessingDecorator - добавление метаданных"),
            ("Facade", "AnalysisFacade - упрощение взаимодействия"),
            ("Strategy", "Sorter - выбор алгоритма"),
            ("Observer", "SystemObserver - мониторинг событий"),
            ("Command", "ImageProcessingCommand - управление операциями"),
        ]
        
        for i, (name, desc) in enumerate(patterns):
            row = i // 3
            col = i % 3
            label = QtWidgets.QLabel(f"✓ {name}")
            label.setToolTip(desc)
            label.setStyleSheet("padding: 8px; background: #e8f5e9; border-radius: 4px; font-weight: bold;")
            patterns_layout.addWidget(label, row, col)
        
        patterns_group.setLayout(patterns_layout)
        layout.addWidget(patterns_group)
        
        # Drone selection
        drone_group = QtWidgets.QGroupBox("Select Drone Type")
        drone_layout = QtWidgets.QHBoxLayout()
        
        self.drone_combo = QtWidgets.QComboBox()
        self.drone_combo.addItems(["Phantom", "Mavic", "Air"])
        self.drone_combo.setMinimumWidth(150)
        
        self.image_count_spin = QtWidgets.QSpinBox()
        self.image_count_spin.setMinimum(1)
        self.image_count_spin.setMaximum(100)
        self.image_count_spin.setValue(5)
        
        drone_layout.addWidget(QtWidgets.QLabel("Drone:"))
        drone_layout.addWidget(self.drone_combo)
        drone_layout.addWidget(QtWidgets.QLabel("Images:"))
        drone_layout.addWidget(self.image_count_spin)
        drone_layout.addStretch()
        
        drone_group.setLayout(drone_layout)
        layout.addWidget(drone_group)
        
        # Analysis button
        button_layout = QtWidgets.QHBoxLayout()
        self.analyze_button = QtWidgets.QPushButton("Start Analysis")
        self.analyze_button.setMinimumHeight(40)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
            QPushButton:pressed {
                background-color: #0d3818;
            }
        """)
        button_layout.addWidget(self.analyze_button)
        layout.addLayout(button_layout)
        
        # Results display
        results_group = QtWidgets.QGroupBox("Analysis Results")
        results_layout = QtWidgets.QVBoxLayout()
        
        self.results_text = QtWidgets.QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # Events log
        log_group = QtWidgets.QGroupBox("System Events (Observer Pattern)")
        log_layout = QtWidgets.QVBoxLayout()
        
        self.events_list = QtWidgets.QListWidget()
        self.events_list.setMaximumHeight(150)
        log_layout.addWidget(self.events_list)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Configuration display
        config_group = QtWidgets.QGroupBox("Configuration (Singleton Pattern)")
        config_layout = QtWidgets.QVBoxLayout()
        
        self.config_text = QtWidgets.QTextEdit()
        self.config_text.setReadOnly(True)
        self.config_text.setMaximumHeight(100)
        config_layout.addWidget(self.config_text)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Update config display
        self.update_config_display()
        
        self.setLayout(layout)
        
    def setup_connections(self):
        """Setup signal-slot connections."""
        self.analyze_button.clicked.connect(self.on_analyze)
        self.event_logged.connect(self.on_event_logged)
        self.analysis_completed.connect(self.on_analysis_completed)
        
    def on_analyze(self):
        """Handle analysis button click."""
        drone_type = self.drone_combo.currentText().lower()
        image_count = self.image_count_spin.value()
        
        self.results_text.clear()
        self.results_text.append(f"Starting analysis for {drone_type.upper()} with {image_count} images...\n")
        
        # Run analysis
        try:
            result = self.drone_app.run_analysis(drone_type, image_count)
            self.analysis_completed.emit(result)
        except Exception as e:
            self.results_text.append(f"Error: {str(e)}")
            logger.error("Analysis error: %s", e, exc_info=True)
    
    def on_analysis_completed(self, result):
        """Handle analysis completion."""
        text = "Analysis Results:\n"
        text += f"Drone Model: {result['drone']['model']}\n"
        text += f"Sensors: {', '.join(result['drone']['sensors'])}\n"
        text += f"Images processed: {len(result['images'])}\n"
        text += f"Output format: {result['output_format']}\n"
        text += f"Processing params: {result['processing_params']}\n"
        
        self.results_text.append(text)
    
    def on_event_logged(self, event):
        """Handle system event."""
        self.events_list.insertItem(0, event)
        # Keep only last 10 events
        while self.events_list.count() > 10:
            self.events_list.takeItem(self.events_list.count() - 1)
    
    def update_config_display(self):
        """Update configuration display from Singleton."""
        cfg = ImageProcessingConfig()
        config_text = f"""Configuration (Singleton Pattern):
• Sort Strategy: {cfg.sort_strategy.__name__}
• Quality: {cfg.quality}
• Available Drones: {', '.join(cfg.drone_models)}
"""
        self.config_text.setText(config_text)


class DroneAnalysisWindow(QtWidgets.QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Image Analysis - Design Patterns Demo")
        self.setGeometry(100, 100, 1000, 900)
        
        # Create central widget
        central_widget = QtWidgets.QScrollArea()
        self.analysis_widget = DroneAnalysisWidget()
        central_widget.setWidget(self.analysis_widget)
        central_widget.setWidgetResizable(True)
        
        self.setCentralWidget(central_widget)
        
        # Setup menu bar
        self.setup_menu()
        
    def setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
    def show_about(self):
        """Show about dialog."""
        QtWidgets.QMessageBox.about(
            self,
            "About",
            "Drone Image Analysis System\n\n"
            "Demonstrates 9 Design Patterns:\n"
            "• Singleton, Factory, Builder (Creational)\n"
            "• Adapter, Decorator, Facade (Structural)\n"
            "• Strategy, Observer, Command (Behavioral)\n\n"
            "Version 1.0"
        )


def main():
    """Main entry point for UI application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = QtWidgets.QApplication(sys.argv)
    window = DroneAnalysisWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
