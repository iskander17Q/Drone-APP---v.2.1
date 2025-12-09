#!/usr/bin/env python3
"""
Drone Image Analysis System - Graphical User Interface (Tkinter-based)
No external dependencies required except the application module
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from pathlib import Path
import sys
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import application
sys.path.insert(0, str(Path(__file__).parent))
from application import DroneAPP


class DroneAnalysisGUI:
    """Main GUI application for Drone Image Analysis"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 Drone Image Analysis System")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)
        
        # Initialize application backend
        self.app = DroneAPP()
        
        # Configure window
        self.root.configure(bg='#f0f0f0')
        
        # Create widgets
        self.create_widgets()
        
        logger.info("GUI initialized successfully")
    
    def create_widgets(self):
        """Create main GUI widgets"""
        # Top frame - Title
        top_frame = tk.Frame(self.root, bg='#2E7D32', height=60)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        top_frame.pack_propagate(False)
        
        title = tk.Label(top_frame, text="🚁 Drone Image Analysis System", 
                        bg='#2E7D32', fg='white', font=('Arial', 18, 'bold'))
        title.pack(pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side - Settings
        left_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        settings_title = tk.Label(left_frame, text="⚙️ Параметры", 
                                 bg='#ffffff', fg='#2E7D32', font=('Arial', 12, 'bold'))
        settings_title.pack(pady=10, padx=10)
        
        # Drone type selection
        tk.Label(left_frame, text="Тип дрона:", bg='#ffffff', font=('Arial', 10)).pack(anchor=tk.W, padx=15, pady=(10, 5))
        self.drone_var = tk.StringVar(value="phantom")
        drone_frame = tk.Frame(left_frame, bg='#ffffff')
        drone_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        for drone in ["phantom", "mavic", "air"]:
            tk.Radiobutton(drone_frame, text=drone.capitalize(), variable=self.drone_var, 
                          value=drone, bg='#ffffff', font=('Arial', 10)).pack(anchor=tk.W)
        
        # Image count
        tk.Label(left_frame, text="Количество изображений:", bg='#ffffff', font=('Arial', 10)).pack(anchor=tk.W, padx=15, pady=(10, 5))
        frame = tk.Frame(left_frame, bg='#ffffff')
        frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        tk.Label(frame, text="1", bg='#ffffff').pack(side=tk.LEFT)
        self.image_scale = tk.Scale(frame, from_=1, to=100, orient=tk.HORIZONTAL, bg='#ffffff', 
                                   length=150, command=lambda x: self.update_image_label())
        self.image_scale.set(5)
        self.image_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.image_label = tk.Label(frame, text="5", bg='#ffffff', width=3)
        self.image_label.pack(side=tk.LEFT)
        
        # Quality
        tk.Label(left_frame, text="Качество обработки:", bg='#ffffff', font=('Arial', 10)).pack(anchor=tk.W, padx=15, pady=(10, 5))
        self.quality_var = tk.StringVar(value="high")
        quality_frame = tk.Frame(left_frame, bg='#ffffff')
        quality_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        for quality in ["low", "medium", "high"]:
            tk.Radiobutton(quality_frame, text=quality.capitalize(), variable=self.quality_var, 
                          value=quality, bg='#ffffff', font=('Arial', 10)).pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg='#ffffff')
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Button(button_frame, text="▶ Анализ", command=self.run_analysis,
                 bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), width=18).pack(fill=tk.X, pady=5)
        tk.Button(button_frame, text="⚡ Демо", command=self.run_auto_demo,
                 bg='#FF9800', fg='white', font=('Arial', 11, 'bold'), width=18).pack(fill=tk.X, pady=5)
        tk.Button(button_frame, text="🗑 Очистить", command=self.clear_results,
                 bg='#f44336', fg='white', font=('Arial', 11, 'bold'), width=18).pack(fill=tk.X, pady=5)
        
        # Right side - Results
        right_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        results_title = tk.Label(right_frame, text="📊 Результаты", 
                                bg='#ffffff', fg='#2E7D32', font=('Arial', 12, 'bold'))
        results_title.pack(pady=10, padx=10)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(right_frame, bg='#ffffff')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(text_frame, height=20, width=60, wrap=tk.WORD,
                                   bg='#fafafa', fg='#333333', font=('Courier', 9),
                                   yscrollcommand=scrollbar.set)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)
        
        # Bottom status bar
        self.status_var = tk.StringVar(value="Готово к работе")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             bg='#e0e0e0', fg='#333333', font=('Arial', 9),
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_image_label(self):
        """Update image count label"""
        self.image_label.config(text=str(self.image_scale.get()))
    
    def run_analysis(self):
        """Run image analysis in background thread"""
        def analyze():
            try:
                self.status_var.set("⏳ Выполняется анализ...")
                self.root.update()
                
                drone_type = self.drone_var.get()
                image_count = self.image_scale.get()
                
                logger.info(f"Starting analysis: drone={drone_type}, images={image_count}")
                
                result = self.app.run_analysis(drone_type, image_count)
                self.display_results(result, drone_type, image_count)
                
                self.status_var.set("✅ Анализ завершён успешно")
                messagebox.showinfo("Успешно", "Анализ завершён!")
                
            except Exception as e:
                logger.error(f"Analysis error: {e}", exc_info=True)
                self.status_var.set("❌ Ошибка при анализе")
                messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
        
        thread = threading.Thread(target=analyze, daemon=True)
        thread.start()
    
    def display_results(self, result, drone_type, image_count):
        """Display analysis results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "📋 РЕЗУЛЬТАТЫ АНАЛИЗА\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        if 'drone' in result:
            drone_info = result['drone']
            self.results_text.insert(tk.END, f"🚁 Модель: {drone_info.get('model', 'Unknown')}\n")
            self.results_text.insert(tk.END, f"📡 Сенсоры: {', '.join(drone_info.get('sensors', []))}\n\n")
        
        self.results_text.insert(tk.END, f"🖼️ Изображений: {image_count}\n")
        if 'processing_params' in result:
            for key, value in result['processing_params'].items():
                self.results_text.insert(tk.END, f"⚙️ {key}: {value}\n")
        
        self.results_text.insert(tk.END, f"\n📊 Формат: {result.get('output_format', 'Unknown')}\n")
        
        if 'images' in result:
            self.results_text.insert(tk.END, f"\n📁 Обработанные файлы:\n")
            for img in result['images']:
                self.results_text.insert(tk.END, f"  • {img}\n")
        
        self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.results_text.config(state=tk.DISABLED)
        self.results_text.see(tk.END)
    
    def clear_results(self):
        """Clear results display"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Результаты очищены")
    
    def run_auto_demo(self):
        """Run automatic demo in background thread"""
        def demo():
            try:
                self.clear_results()
                self.status_var.set("⏳ Автодемонстрация...")
                self.root.update()
                
                self.results_text.config(state=tk.NORMAL)
                self.results_text.insert(tk.END, "🎬 АВТОДЕМОНСТРАЦИЯ СИСТЕМЫ\n")
                self.results_text.insert(tk.END, "=" * 60 + "\n\n")
                
                drone_types = ["phantom", "mavic", "air"]
                image_counts = [5, 3, 7]
                
                for drone_type, image_count in zip(drone_types, image_counts):
                    self.results_text.insert(tk.END, f"▶ {drone_type.upper()} ({image_count} фото)\n")
                    self.results_text.insert(tk.END, "-" * 40 + "\n")
                    
                    result = self.app.run_analysis(drone_type, image_count)
                    
                    if 'drone' in result:
                        self.results_text.insert(tk.END, f"  Модель: {result['drone'].get('model', 'Unknown')}\n")
                        self.results_text.insert(tk.END, f"  Сенсоры: {', '.join(result['drone'].get('sensors', []))}\n")
                    
                    if 'images' in result:
                        self.results_text.insert(tk.END, f"  Обработано: {len(result['images'])} файлов\n")
                    
                    self.results_text.insert(tk.END, f"  Формат: {result.get('output_format', 'Unknown')}\n\n")
                    self.root.update()
                
                self.results_text.insert(tk.END, "=" * 60 + "\n")
                self.results_text.insert(tk.END, "✅ Демонстрация завершена!\n")
                self.results_text.config(state=tk.DISABLED)
                self.results_text.see(tk.END)
                
                self.status_var.set("✅ Демонстрация завершена")
                messagebox.showinfo("Успешно", "Демонстрация завершена!")
                
            except Exception as e:
                logger.error(f"Demo error: {e}", exc_info=True)
                self.status_var.set("❌ Ошибка")
                messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
        
        thread = threading.Thread(target=demo, daemon=True)
        thread.start()


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = DroneAnalysisGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = DroneAnalysisGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
