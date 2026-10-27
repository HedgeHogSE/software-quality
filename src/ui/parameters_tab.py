"""
Вкладка параметров модели.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from src.model.parameters import get_variables_order, get_initial_values, get_max_values, PARAMETERS

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
        
        # Строка 0: Выбор реализации
        ttk.Label(self.scrollable_frame, text="Реализация:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        impl_combo = ttk.Combobox(self.scrollable_frame, textvariable=self.current_implementation, values=["1", "2", "3", "4", "5"], width=10, state="readonly")
        impl_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        impl_combo.bind("<<ComboboxSelected>>", lambda e: self._load_implementation())
        impl_combo.current(0)
        
        # Строка 1: Заголовки
        ttk.Label(self.scrollable_frame, text="Переменная").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.scrollable_frame, text="Описание").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(self.scrollable_frame, text="Значение").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Label(self.scrollable_frame, text="Максимум").grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Сконфигурировать колонки
        self.scrollable_frame.columnconfigure(1, weight=1)
        
        # Поля ввода для каждой переменной (строки 2 и дальше)
        self.max_entries: Dict[str, tk.Entry] = {}
        
        for i, var in enumerate(self.variables, start=2):
            desc = VARIABLE_DESCRIPTIONS.get(var, '')
            ttk.Label(self.scrollable_frame, text=var).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            ttk.Label(self.scrollable_frame, text=desc).grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            # Начальное значение
            entry = ttk.Entry(self.scrollable_frame, width=15)
            entry.grid(row=i, column=2, padx=5, pady=2, sticky="w")
            self.entries[var] = entry
            
            # Максимум - будет установлен при загрузке реализации
            max_entry = ttk.Entry(self.scrollable_frame, width=15)
            max_entry.grid(row=i, column=3, padx=5, pady=2, sticky="w")
            self.max_entries[var] = max_entry
        
        # Строка после всех переменных: Кнопка установки значений
        row_btn = 2 + len(self.variables)
        ttk.Button(
            self.scrollable_frame,
            text="Загрузить выбранную реализацию",
            command=self._set_default_values
        ).grid(row=row_btn, column=0, columnspan=4, pady=10)
        
        # Блок с формулами функций
        row_formulas = row_btn + 1
        formulas_frame = ttk.LabelFrame(self.scrollable_frame, text="Формулы функций модели")
        formulas_frame.grid(row=row_formulas, column=0, columnspan=4, pady=10, sticky="w")
        
        formulas_text = """Типы функций:
  f(x) = a*x + b           (линейная)
  f(x) = a*x^2 + b*x + c   (квадратичная)
  f(x) = a*x^3 + b*x^2 + c*x + d   (кубическая)

Известные функции из документа:
  f3(x)   = 0.2*x^3 + 0.8*x^2 + 0.2*x + 0.09
  f5(x)   = 0.25*x + 0.5
  f9(x)   = 0.7*x^2 + (-0.4)*x + 0.24
  f48(x)  = 0.53*x + 0.17
  f72(x)  = 0.5*x^2 + 0.27*x + 0.9
  f81(x)  = 0.28*x + (-0.63)
  f117(x) = 0.72*x^2 + 0.12*x + 0.8

Остальные функции f1-f187 по умолчанию: f(x) = x
"""
        
        formulas_label = tk.Label(formulas_frame, text=formulas_text, justify="left", font=("Courier New", 9), bg="white", relief="solid", padx=5, pady=5)
        formulas_label.pack(fill="both", expand=True, padx=5, pady=5)
        
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
        max_vals = get_max_values(impl)
        for var, val, max_val in zip(self.variables, values, max_vals):
            self.entries[var].delete(0, tk.END)
            self.entries[var].insert(0, str(val))
            self.max_entries[var].delete(0, tk.END)
            self.max_entries[var].insert(0, str(max_val))
    
    def _set_default_values(self):
        """Установить начальные значения и максимумы для текущей выбранной реализации."""
        impl = self.current_implementation.get()
        values = get_initial_values(impl)
        max_vals = get_max_values(impl)
        for var, val, max_val in zip(self.variables, values, max_vals):
            self.entries[var].delete(0, tk.END)
            self.entries[var].insert(0, str(val))
            self.max_entries[var].delete(0, tk.END)
            self.max_entries[var].insert(0, str(max_val))
    
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