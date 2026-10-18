"""
Вкладка параметров модели.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from src.model.parameters import get_variables_order, get_initial_values, PARAMETERS

# Описания переменных состояния
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


class ParametersTab(ttk.Frame):
    """Вкладка для настройки параметров модели."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.variables = get_variables_order()
        self.current_implementation = tk.IntVar(value=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создать виджеты вкладки."""
        # Список параметров
        self.params_frame = ttk.LabelFrame(self, text="Параметры состояния")
        self.params_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создать таблицу параметров
        self.entries: Dict[str, tk.Entry] = {}
        
        # Canvas для прокрутки
        canvas = tk.Canvas(self.params_frame)
        scrollbar = ttk.Scrollbar(self.params_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Заголовки
        ttk.Label(self.scrollable_frame, text="Переменная").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Описание").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Значение").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Максимум").grid(row=0, column=3, padx=5, pady=5)
        
        # Выбор реализации
        ttk.Label(self.scrollable_frame, text="Реализация:").grid(row=len(self.variables) + 2, column=0, padx=5, pady=5, sticky="w")
        impl_combo = ttk.Combobox(self.scrollable_frame, textvariable=self.current_implementation, values=["1", "2", "3", "4", "5"], width=10, state="readonly")
        impl_combo.grid(row=len(self.variables) + 2, column=1, padx=5, pady=5, sticky="w")
        impl_combo.bind("<<ComboboxSelected>>", lambda e: self._load_implementation())
        impl_combo.current(0)
        
        # Сконфигурировать колонки
        self.scrollable_frame.columnconfigure(1, weight=1)  # Колонка описаний растягивается
        
        # Поля ввода для каждой переменной
        self.max_entries: Dict[str, tk.Entry] = {}
        
        for i, var in enumerate(self.variables, start=1):
            desc = VARIABLE_DESCRIPTIONS.get(var, '')
            ttk.Label(self.scrollable_frame, text=var).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            ttk.Label(self.scrollable_frame, text=desc).grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            # Начальное значение
            entry = ttk.Entry(self.scrollable_frame, width=15)
            entry.grid(row=i, column=2, padx=5, pady=2, sticky="w")
            self.entries[var] = entry
            
            # Максимум
            max_entry = ttk.Entry(self.scrollable_frame, width=15)
            max_entry.grid(row=i, column=3, padx=5, pady=2, sticky="w")
            max_entry.insert(0, "1.0")  # По умолчанию 1.0
            self.max_entries[var] = max_entry
        
        # Кнопка установки начальных значений
        ttk.Button(
            self.scrollable_frame,
            text="Загрузить выбранную реализацию",
            command=self._set_default_values
        ).grid(row=len(self.variables) + 1, column=0, columnspan=4, pady=10)
        
        # Временной интервал
        time_frame = ttk.LabelFrame(self, text="Временной интервал")
        time_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(time_frame, text="Начало:").grid(row=0, column=0, padx=5, pady=5)
        self.t_start_entry = ttk.Entry(time_frame, width=10)
        self.t_start_entry.insert(0, str(PARAMETERS.t_start))
        self.t_start_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(time_frame, text="Конец:").grid(row=0, column=2, padx=5, pady=5)
        self.t_end_entry = ttk.Entry(time_frame, width=10)
        self.t_end_entry.insert(0, str(PARAMETERS.t_end))
        self.t_end_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(time_frame, text="Шаг:").grid(row=0, column=4, padx=5, pady=5)
        self.step_entry = ttk.Entry(time_frame, width=10)
        self.step_entry.insert(0, str(PARAMETERS.step))
        self.step_entry.grid(row=0, column=5, padx=5, pady=5)
    
    def _load_implementation(self):
        """Загрузить начальные значения для выбранной реализации."""
        impl = self.current_implementation.get()
        values = get_initial_values(impl)
        for var, val in zip(self.variables, values):
            self.entries[var].delete(0, tk.END)
            self.entries[var].insert(0, str(val))
    
    def _set_default_values(self):
        """Установить начальные значения и максимумы для текущей выбранной реализации."""
        impl = self.current_implementation.get()
        values = get_initial_values(impl)
        for var, val in zip(self.variables, values):
            self.entries[var].delete(0, tk.END)
            self.entries[var].insert(0, str(val))
            self.max_entries[var].delete(0, tk.END)
            self.max_entries[var].insert(0, "1.0")  # По умолчанию 1.0
    
    def get_parameters(self) -> dict:
        """Получить текущие параметры из интерфейса."""
        params = {
            "t_start": float(self.t_start_entry.get()),
            "t_end": float(self.t_end_entry.get()),
            "step": float(self.step_entry.get()),
            "initial_values": {},
            "max_values": {},
            "implementation": self.current_implementation.get()
        }
        
        for var in self.variables:
            params["initial_values"][var] = float(self.entries[var].get())
            params["max_values"][var] = float(self.max_entries[var].get())
        
        return params