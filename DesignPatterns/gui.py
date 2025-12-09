#!/usr/bin/env python3
"""
Drone Image Analysis System - Graphical User Interface (Tkinter-based)
No external dependencies required except the application module
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from pathlib import Path
import sys

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
        self.root.title("Drone Image Analysis System - Design Patterns")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize application backend
        self.app = DroneAPP()
        
        # Configure styles
        self.configure_styles()
        
        # Create widgets
        self.create_widgets()
        
        # Set window icon and position
        self.root.update_idletasks()
        self.center_window()
        
        logger.info("GUI initialized successfully")
    
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define colors
        bg_color = '#f0f0f0'
        fg_color = '#333333'
        accent_color = '#2E7D32'
        button_color = '#4CAF50'
        
        # Configure main style
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
        style.configure('Title.TLabel', background=bg_color, foreground=accent_color, font=('Arial', 18, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        
        # Configure button style
        style.map('TButton',
                  foreground=[('pressed', '#ffffff'), ('active', '#ffffff')],
                  background=[('pressed', '#2E7D32'), ('active', button_color)])
        
        self.root.configure(bg=bg_color)
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create main GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="🚁 Drone Image Analysis", style='Title.TLabel')
        title.pack(pady=(0, 5))
        
        subtitle = ttk.Label(main_frame, text="Система анализа аэрофотоснимков с паттернами проектирования",
                            style='Subtitle.TLabel')
        subtitle.pack(pady=(0, 20))
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Информация о системе", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = (
            "Система демонстрирует 9 паттернов проектирования:\n"
            "• Singleton - управление конфигурацией\n"
            "• Factory - создание объектов дронов\n"
            "• Builder - построение сложных объектов\n"
            "• Adapter - адаптация интерфейсов\n"
            "• Decorator - расширение функциональности\n"
            "• Facade - упрощение сложной системы\n"
            "• Strategy - выбор алгоритма в runtime\n"
            "• Observer - систем событий\n"
            "• Command - инкапсуляция операций"
        )
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Конфигурация анализа", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Drone type selection
        drone_frame = ttk.Frame(config_frame)
        drone_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(drone_frame, text="Тип дрона:").pack(side=tk.LEFT, padx=(0, 10))
        self.drone_var = tk.StringVar(value="phantom")
        drone_combo = ttk.Combobox(drone_frame, textvariable=self.drone_var,
                                   values=["phantom", "mavic", "air"],
                                   state='readonly', width=20)
        drone_combo.pack(side=tk.LEFT)
        
        # Image count selection
        image_frame = ttk.Frame(config_frame)
        image_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(image_frame, text="Количество изображений:").pack(side=tk.LEFT, padx=(0, 10))
        self.image_var = tk.IntVar(value=5)
        image_spin = ttk.Spinbox(image_frame, from_=1, to=100, textvariable=self.image_var, width=20)
        image_spin.pack(side=tk.LEFT)
        
        # Quality setting
        quality_frame = ttk.Frame(config_frame)
        quality_frame.pack(fill=tk.X)
        
        ttk.Label(quality_frame, text="Качество обработки:").pack(side=tk.LEFT, padx=(0, 10))
        self.quality_var = tk.StringVar(value="high")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                     values=["low", "medium", "high"],
                                     state='readonly', width=20)
        quality_combo.pack(side=tk.LEFT)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="📊 Результаты анализа", padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Results text widget
        self.results_text = tk.Text(results_frame, height=12, width=80, wrap=tk.WORD,
                                    bg='#ffffff', fg='#333333', font=('Courier', 9))
        self.results_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text['yscrollcommand'] = scrollbar.set
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 0))
        
        # Run analysis button
        run_btn = ttk.Button(buttons_frame, text="▶ Запустить анализ",
                            command=self.run_analysis)
        run_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear results button
        clear_btn = ttk.Button(buttons_frame, text="🗑 Очистить результаты",
                              command=self.clear_results)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto demo button
        demo_btn = ttk.Button(buttons_frame, text="⚡ Автодемонстрация",
                             command=self.run_auto_demo)
        demo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Exit button
        exit_btn = ttk.Button(buttons_frame, text="❌ Выход",
                             command=self.root.quit)
        exit_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Готово к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
    
    def run_analysis(self):
        """Run image analysis with selected parameters"""
        try:
            self.status_var.set("⏳ Выполняется анализ...")
            self.root.update()
            
            drone_type = self.drone_var.get()
            image_count = self.image_var.get()
            
            logger.info(f"Starting analysis: drone={drone_type}, images={image_count}")
            
            # Run analysis
            result = self.app.run_analysis(drone_type, image_count)
            
            # Display results
            self.display_results(result, drone_type, image_count)
            
            self.status_var.set("✅ Анализ завершён успешно")
            messagebox.showinfo("Успешно", "Анализ завершён!\nСм. результаты ниже.")
            
        except Exception as e:
            logger.error(f"Analysis error: {e}", exc_info=True)
            self.status_var.set("❌ Ошибка при анализе")
            messagebox.showerror("Ошибка", f"Ошибка при анализе:\n{str(e)}")
    
    def display_results(self, result, drone_type, image_count):
        """Display analysis results in text widget"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, "=" * 80 + "\n")
        self.results_text.insert(tk.END, "📋 РЕЗУЛЬТАТЫ АНАЛИЗА\n")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # Drone info
        self.results_text.insert(tk.END, "🚁 ИНФОРМАЦИЯ О ДРОНЕ:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if 'drone' in result:
            drone_info = result['drone']
            self.results_text.insert(tk.END, f"  Модель: {drone_info.get('model', 'Unknown')}\n")
            self.results_text.insert(tk.END, f"  Сенсоры: {', '.join(drone_info.get('sensors', []))}\n")
        
        # Processing parameters
        self.results_text.insert(tk.END, "\n⚙️ ПАРАМЕТРЫ ОБРАБОТКИ:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        self.results_text.insert(tk.END, f"  Количество изображений: {image_count}\n")
        if 'processing_params' in result:
            params = result['processing_params']
            for key, value in params.items():
                self.results_text.insert(tk.END, f"  {key.capitalize()}: {value}\n")
        
        # Output format
        self.results_text.insert(tk.END, "\n📊 ФОРМАТ ВЫВОДА:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        output_format = result.get('output_format', 'Unknown')
        self.results_text.insert(tk.END, f"  Формат: {output_format}\n")
        
        # Processed images
        self.results_text.insert(tk.END, "\n🖼️ ОБРАБОТАННЫЕ ИЗОБРАЖЕНИЯ:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if 'images' in result:
            for i, image in enumerate(result['images'], 1):
                self.results_text.insert(tk.END, f"  {i}. {image}\n")
        
        self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        self.results_text.config(state=tk.DISABLED)
        self.results_text.see(tk.END)
    
    def clear_results(self):
        """Clear results display"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Результаты очищены")
    
    def run_auto_demo(self):
        """Run automatic demonstration with multiple drones"""
        try:
            self.clear_results()
            self.status_var.set("⏳ Выполняется автодемонстрация...")
            self.root.update()
            
            self.results_text.config(state=tk.NORMAL)
            self.results_text.insert(tk.END, "🎬 АВТОМАТИЧЕСКАЯ ДЕМОНСТРАЦИЯ СИСТЕМЫ\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            
            # Test all drone types
            drone_types = ["phantom", "mavic", "air"]
            image_counts = [5, 3, 7]
            
            for drone_type, image_count in zip(drone_types, image_counts):
                self.results_text.insert(tk.END, f"\n▶ Анализ для дрона: {drone_type.upper()}\n")
                self.results_text.insert(tk.END, "-" * 40 + "\n")
                
                result = self.app.run_analysis(drone_type, image_count)
                
                if 'drone' in result:
                    drone_info = result['drone']
                    self.results_text.insert(tk.END, f"  Модель: {drone_info.get('model', 'Unknown')}\n")
                    self.results_text.insert(tk.END, f"  Сенсоры: {', '.join(drone_info.get('sensors', []))}\n")
                
                if 'images' in result:
                    self.results_text.insert(tk.END, f"  Обработано изображений: {len(result['images'])}\n")
                
                self.results_text.insert(tk.END, f"  Формат вывода: {result.get('output_format', 'Unknown')}\n")
                self.results_text.insert(tk.END, "\n")
                
                self.root.update()
            
            self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.results_text.insert(tk.END, "✅ Автодемонстрация завершена!\n")
            self.results_text.config(state=tk.DISABLED)
            self.results_text.see(tk.END)
            
            self.status_var.set("✅ Автодемонстрация завершена")
            messagebox.showinfo("Успешно", "Автодемонстрация завершена!")
            
        except Exception as e:
            logger.error(f"Demo error: {e}", exc_info=True)
            self.status_var.set("❌ Ошибка при демонстрации")
            messagebox.showerror("Ошибка", f"Ошибка при демонстрации:\n{str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = DroneAnalysisGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
