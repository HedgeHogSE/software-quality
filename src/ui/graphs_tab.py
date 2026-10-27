"""
Вкладка графиков для отображения результатов моделирования.
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

from src.model.disturbances import DISTURBANCES


class GraphsTab(ttk.Frame):
    """Вкладка для отображения графиков."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.result = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создать виджеты вкладки."""
        # Рамка для управления графиками
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(control_frame, text="Выберите переменные:").pack(side="left", padx=5)
        
        self.variables = [
            'u5', 'u24', 'u25', 'u26', 'u27', 'u28', 'u54', 'u55', 'u56',
            'u107', 'u108', 'u109', 'u110', 'u111', 'u112', 'u113', 'u114', 'u115',
            'u116', 'u117', 'u118', 'u119', 'u120', 'u121', 'u122', 'u123', 'u124', 'u125'
        ]
        
        self.selected_vars = tk.Listbox(
            control_frame,
            selectmode="multiple",
            height=5,
            exportselection=False
        )
        for var in self.variables:
            self.selected_vars.insert(tk.END, var)
            self.selected_vars.selection_set(0)
        self.selected_vars.pack(side="left", padx=5)
        
        ttk.Button(
            control_frame,
            text="Построить график",
            command=self._plot_graph
        ).pack(side="left", padx=5)
        
        # Canvas для графика
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def _plot_graph(self):
        """Построить график выбранных переменных."""
        if self.result is None:
            self.ax.clear()
            self.ax.set_title("Сначала запустите симуляцию")
            self.canvas.draw()
            return
        
        # Получить выбранные переменные
        selected_indices = self.selected_vars.curselection()
        selected_vars = [self.variables[i] for i in selected_indices]
        
        if not selected_vars:
            return
        
        # Очистить график
        self.ax.clear()
        
        # Построить графики
        t = self.result.t
        for var in selected_vars:
            var_idx = self.variables.index(var)
            values = self.result.u[var_idx, :]
            self.ax.plot(t, values, label=var)
        
        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Значение")
        self.ax.set_title("Динамика характеристик качества ПО")
        self.ax.legend()
        self.ax.grid(True)
        
        self.canvas.draw()
    
    def set_result(self, result):
        """Установить результат для отображения."""
        self.result = result