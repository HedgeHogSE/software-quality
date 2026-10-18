"""
Главный модуль приложения моделирования качества ПО.
"""
import sys
import os

# Добавить корневую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from tkinter import ttk

from src.ui.parameters_tab import ParametersTab
from src.ui.graphs_tab import GraphsTab
from src.ui.disturbances_tab import DisturbancesTab
from src.ui.state_table import StateRadarCharts
from src.services.simulation_service import SimulationService
from src.model.parameters import get_variables_order


class QualityApp(ttk.Notebook):
    """Основное окно приложения с вкладками."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Моделирование качества ПО (ISO)")
        self.parent.geometry("1000x700")
        
        self.service = SimulationService()
        self.variables = get_variables_order()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Настроить интерфейс."""
        # Вкладки
        self.parameters_tab = ParametersTab(self)
        self.graphs_tab = GraphsTab(self)
        self.disturbances_tab = DisturbancesTab(self)
        self.state_radar = StateRadarCharts(self, self.variables)
        
        self.add(self.parameters_tab, text="Параметры")
        self.add(self.graphs_tab, text="Графики")
        self.add(self.disturbances_tab, text="Возмущения")
        self.add(self.state_radar, text="Диаграммы состояния")
        
        # Кнопка запуска моделирования
        button_frame = ttk.Frame(self.parameters_tab)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(
            button_frame,
            text="Запустить модель",
            command=self._run_simulation
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Сохранить результаты",
            command=self._save_results
        ).pack(side="left", padx=5)
    
    def _run_simulation(self):
        """Запустить модель для выбранной реализации."""
        params = self.parameters_tab.get_parameters()
        impl = params.get("implementation", 1)
        
        result = self.service.run_simulation(
            implementation=impl,
            t_start=params["t_start"],
            t_end=params["t_end"],
            step=params["step"]
        )
        
        self.graphs_tab.set_result(result)
        
        # Обновить диаграммы состояния
        self.state_radar.set_result(result, params["max_values"])
    
    def _save_results(self):
        """Сохранить результаты (заглушка)."""
        print("Сохранение результатов...")


if __name__ == "__main__":
    root = tk.Tk()
    app = QualityApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()