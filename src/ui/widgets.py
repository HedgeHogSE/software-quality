"""
Базовые виджеты для GUI приложения.
"""
import tkinter as tk
from tkinter import ttk
from typing import List


class VariableSelector(ttk.Frame):
    """Выбор переменных для отображения на графике."""
    
    def __init__(self, parent, variables: List[str], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.variables = variables
        self.selected = {v: tk.BooleanVar(value=True) for v in variables}
        
        # Создать список с чекбоксами
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Добавить чекбоксы
        row = 0
        for var in variables:
            cb = ttk.Checkbutton(
                self.scrollable_frame,
                text=var,
                variable=self.selected[var]
            )
            cb.grid(row=row, column=0, sticky="w", padx=5, pady=2)
            row += 1
    
    def get_selected_variables(self) -> List[str]:
        """Получить список выбранных переменных."""
        return [v for v, var in self.selected.items() if var.get()]