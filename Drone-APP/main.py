import sys
import os
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

# Импортируем функции анализа из analysis.py
from analysis import load_image, compute_indices, generate_heatmap, classify_index
from utils import get_gps_from_image, generate_pdf_report

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мониторинг состояния полей")
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет и основной layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Панель кнопок (верхняя)
        button_layout = QtWidgets.QHBoxLayout()
        
        self.btn_load = QtWidgets.QPushButton("Загрузить изображение")
        self.btn_load.clicked.connect(self.load_image_file)
        button_layout.addWidget(self.btn_load)
        
        self.btn_analyze = QtWidgets.QPushButton("Анализировать")
        self.btn_analyze.clicked.connect(self.analyze_image)
        self.btn_analyze.setEnabled(False)
        button_layout.addWidget(self.btn_analyze)
        
        self.btn_save = QtWidgets.QPushButton("Сохранить отчет (PDF)")
        self.btn_save.clicked.connect(self.save_report)
        self.btn_save.setEnabled(False)
        button_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(button_layout)
        
        # Отображение исходного изображения
        self.label_original = QtWidgets.QLabel("Исходное изображение")
        self.label_original.setAlignment(QtCore.Qt.AlignCenter)
        self.label_original.setFixedHeight(250)
        self.label_original.setStyleSheet("border: 1px solid black;")
        main_layout.addWidget(self.label_original)
        
        # Отображение тепловой карты
        self.label_heatmap = QtWidgets.QLabel("Тепловая карта")
        self.label_heatmap.setAlignment(QtCore.Qt.AlignCenter)
        self.label_heatmap.setFixedHeight(250)
        self.label_heatmap.setStyleSheet("border: 1px solid black;")
        main_layout.addWidget(self.label_heatmap)
        
        # Текстовый отчет
        self.text_report = QtWidgets.QTextEdit()
        self.text_report.setReadOnly(True)
        main_layout.addWidget(self.text_report)
        
        # Храним пути и данные
        self.current_image_path = None
        self.current_heatmap_path = None
        self.current_stats = None
        self.current_gps = None
        
        # Создаём меню
        self.create_menus()

    def create_menus(self):
        """Создаёт меню в строке меню."""
        menu_bar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        action_save_pdf = QtWidgets.QAction("Сохранить отчет (PDF)", self)
        action_save_pdf.triggered.connect(self.save_report)
        file_menu.addAction(action_save_pdf)
        
        # Меню "Экспорт"
        export_menu = menu_bar.addMenu("Экспорт")
        action_export_spectra = QtWidgets.QAction("Сохранить спектральные карты", self)
        action_export_spectra.triggered.connect(self.export_spectral_maps)
        export_menu.addAction(action_export_spectra)

    def load_image_file(self):
        """Загрузка файла изображения с диска."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выбрать изображение",
            "",
            "Изображения (*.jpg *.jpeg *.png *.bmp *.raw *.dng *.nef *.cr2 *.arw)"
        )
        if file_path:
            self.current_image_path = file_path
            # Отображаем исходное изображение в label
            pixmap = QtGui.QPixmap(file_path)
            if not pixmap.isNull():
                if (pixmap.width() > self.label_original.width() or 
                    pixmap.height() > self.label_original.height()):
                    pixmap = pixmap.scaled(self.label_original.size(), 
                                           QtCore.Qt.KeepAspectRatio,
                                           QtCore.Qt.SmoothTransformation)
                self.label_original.setPixmap(pixmap)
            else:
                self.label_original.setText("Не удалось отобразить изображение.")
            
            self.label_heatmap.clear()
            self.text_report.clear()
            
            self.btn_analyze.setEnabled(True)
            # Попытка извлечь GPS-данные
            self.current_gps = get_gps_from_image(file_path)
            if self.current_gps:
                gps_text = f"GPS: {self.current_gps.get('latitude', 'N/A')}, {self.current_gps.get('longitude', 'N/A')}"
            else:
                gps_text = "GPS: не обнаружены"
            self.statusBar().showMessage(gps_text)

    def analyze_image(self):
        """Запускает анализ индексов и отображает тепловую карту."""
        if not self.current_image_path:
            return
        
        try:
            # Загружаем изображение и считаем индексы
            image = load_image(self.current_image_path)
            indices = compute_indices(image)
            
            # Используем один из индексов для отображения тепловой карты
            index_map = indices.get("NDVI_emp")
            if index_map is None:
                index_map = list(indices.values())[0]
            
            # Генерируем тепловую карту (в папке assets)
            os.makedirs("assets", exist_ok=True)
            heatmap_filename = os.path.join("assets", "heatmap_temp.png")
            generate_heatmap(index_map, heatmap_filename)
            self.current_heatmap_path = heatmap_filename
            
            # Отображаем тепловую карту в label
            pixmap = QtGui.QPixmap(heatmap_filename)
            if not pixmap.isNull():
                if (pixmap.width() > self.label_heatmap.width() or 
                    pixmap.height() > self.label_heatmap.height()):
                    pixmap = pixmap.scaled(self.label_heatmap.size(),
                                           QtCore.Qt.KeepAspectRatio,
                                           QtCore.Qt.SmoothTransformation)
                self.label_heatmap.setPixmap(pixmap)
            else:
                self.label_heatmap.setText("Не удалось отобразить тепловую карту.")
            
            # Классифицируем состояние поля
            stats, conclusion = classify_index(index_map)
            self.current_stats = stats  # сохраняем, если нужно
            
            # Формируем текст отчёта
            report_text = "Распределение состояния растений:\n"
            for category, pct in stats.items():
                report_text += f"{category}: {pct:.1f}%\n"
            report_text += "\nВывод: " + conclusion
            self.text_report.setText(report_text)
            
            # Активируем кнопку сохранения PDF
            self.btn_save.setEnabled(True)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при анализе: {str(e)}")

    def save_report(self):
        """Сохраняет PDF-отчет с использованием функции generate_pdf_report из utils.py."""
        if not self.current_image_path or not self.current_heatmap_path:
            return
        
        pdf_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Сохранить отчет",
            "",
            "PDF Files (*.pdf)"
        )
        if pdf_path:
            try:
                generate_pdf_report(
                    pdf_path,
                    self.current_image_path,
                    self.current_heatmap_path,
                    self.text_report.toPlainText(),
                    self.current_gps,
                    index_type="NDVI_emp"
                )
                QtWidgets.QMessageBox.information(self, "Успех", "Отчет успешно сохранен!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении отчета: {str(e)}")

    def export_spectral_maps(self):
        """Сохраняет все доступные спектральные карты в выбранную папку."""
        if not self.current_image_path:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Сначала загрузите изображение.")
            return

        export_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if not export_dir:
            return
        
        try:
            image = load_image(self.current_image_path)
            indices = compute_indices(image)
            
            for index_name, index_map in indices.items():
                output_path = os.path.join(export_dir, f"{index_name}.png")
                generate_heatmap(index_map, output_path)
            
            QtWidgets.QMessageBox.information(self, "Готово",
                                              f"Спектральные карты сохранены в: {export_dir}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", 
                                           f"Ошибка при экспорте спектральных карт: {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()