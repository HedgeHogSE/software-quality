"""
Радар-диаграммы состояния системы в контрольных точках.
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


VARIABLE_DESCRIPTIONS = {
    'u5': 'Сопровождаемость',
    'u24': 'Анализируемость',
    'u25': 'Изменяемость',
    'u26': 'Стабильность',
    'u27': 'Тестируемость',
    'u28': 'Согласованность',
    'u54': 'Не соотв. документации',
    'u55': 'Не соотв. форм документов',
    'u56': 'Отсутствие лицензии',
    'u107': 'Низкий уровень языка',
    'u108': 'Отсутствие схемы модулей',
    'u109': 'Низкая читабельность кода',
    'u110': 'Недостаточно комментариев',
    'u111': 'Отсутствие системного подхода',
    'u112': 'Слишком большие модули',
    'u113': 'Недостатки диагностики',
    'u114': 'Недостаточность регистрации',
    'u115': 'Высокая трудоемкость изменений',
    'u116': 'Низкая параметризация',
    'u117': 'Низкая локальность модификации',
    'u118': 'Вторичные дефекты',
    'u119': 'Недостаточность требований к тестированию',
    'u120': 'Отсутствие описания методов испытаний',
    'u121': 'Невозможность объективного теста',
    'u122': 'Невозможность использования инструментов тестирования',
    'u123': 'Не соотв. стандартам сопровождения',
    'u124': 'Не соотв. требованиям к исходным текстам',
    'u125': 'Отсутствие регистрации изменений',
}


class StateRadarCharts(ttk.Frame):
    """Радар-диаграммы состояния системы в контрольных точках."""
    
    def __init__(self, parent, variables: list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.variables = variables
        self.current_chart_idx = tk.IntVar(value=0)
        self.result = None
        self._control_times = []
        self._chart_labels = ["t=0.00 (начало)", "t=0.25 (1 четверть)", "t=0.50 (середина)", 
                              "t=0.75 (3 четверть)", "t=1.00 (конец)"]
        self.max_values = None  # Максимальные значения для границы
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создать виджеты для отображения радар-диаграмм."""
        # Рамка для переключения
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(control_frame, text="Контрольная точка:").pack(side="left", padx=5)
        
        self.combo = ttk.Combobox(
            control_frame,
            values=self._chart_labels,
            width=30,
            state="readonly"
        )
        self.combo.current(0)
        self.combo.pack(side="left", padx=5)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._on_chart_selected())
        
        # Canvas для диаграмм
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_radar_chart(self, values, title, max_values=None):
        """Создать радар-диаграмму для одного набора значений."""
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111, polar=True)
        
        # Углы для каждой переменной
        n_vars = len(values)
        angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
        angles += angles[:1]  # Замкнуть круг
        
        # Значения
        values = list(values) + [values[0]]
        
        # Построить основную диаграмму
        ax.plot(angles, values, 'o-', linewidth=2, label='Качество')
        ax.fill(angles, values, alpha=0.25, label='Текущее состояние')
        
        # Построить диаграмму границ (красная)
        if max_values is not None:
            max_values_list = []
            for var in self.variables:
                max_val = max_values.get(var, 1.0)
                max_values_list.append(max_val)
            max_values_list = max_values_list + [max_values_list[0]]
            ax.plot(angles, max_values_list, 'r--', linewidth=2, label='Граница')
        
        # Настройки
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([self.variables[i] for i in range(n_vars)], fontsize=6)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['0.25', '0.5', '0.75', '1.0'], fontsize=8)
        ax.set_title(title, size=12, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        return fig
    
    def _on_chart_selected(self):
        """Обработчик выбора контрольной точки."""
        selected_label = self.combo.get()
        if selected_label in self._chart_labels:
            self.current_chart_idx.set(self._chart_labels.index(selected_label))
            self._draw_chart()
    
    def _draw_chart(self):
        """Отрисовать выбранную диаграмму."""
        # Очистить старые диаграммы
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        t_idx = self.current_chart_idx.get()
        
        if hasattr(self, 'result') and self.result is not None:
            if 0 <= t_idx < len(self.result.t):
                values = self.result.u[:, t_idx]
                values = np.clip(values, 0.0, 1.0)
                title = f"Состояние системы в момент t={self.result.t[t_idx]:.2f}"
                
                fig = self._create_radar_chart(values, title, self.max_values)
                
                canvas = FigureCanvasTkAgg(fig, self.canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
            else:
                ttk.Label(self.canvas_frame, text="Нет данных для выбранной точки").pack()
        else:
            ttk.Label(self.canvas_frame, text="Сначала запустите симуляцию").pack()
    
    def set_result(self, result, max_values=None):
        """Установить результат для отображения."""
        self.result = result
        self.max_values = max_values
        self._draw_chart()