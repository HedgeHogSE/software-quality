"""
Вкладка отображения внешних возмущений.
"""
import tkinter as tk
from tkinter import ttk
import math

from src.model.disturbances import DISTURBANCES, fak1, fak2, fak3, fak4, fak5, fak6


class DisturbancesTab(ttk.Frame):
    """Вкладка для отображения внешних возмущений."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        
        self.disturbances = {
            1: ("Fak1(t) = t² + 1", fak1),
            2: ("Fak2(t) = cos²(1.5πt - π/6) / 4 + 0.2", fak2),
            3: ("Fak3(t) = sin(sin(πt - π/6)) / 2.5 + 0.3", fak3),
            4: ("Fak4(t) = 2t - 1", fak4),
            5: ("Fak5(t) = sin²(πt - π/6) / 2.5 + 0.3", fak5),
            6: ("Fak6(t) = гармоническая функция [0.3, 0.7]", fak6),
        }
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создать виджеты вкладки."""
        # Заголовок
        ttk.Label(
            self,
            text="Внешние возмущения",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Список возмущений
        self.listbox = tk.Listbox(self, width=80, height=15)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Описание каждого возмущения
        descriptions = [
            "1. Fak1 - Опыт разработчиков программного комплекса",
            "2. Fak2 - Опыт работы эксплуатационного персонала",
            "3. Fak3 - Трудоёмкость разработки программного обеспечения",
            "4. Fak4 - Курс рубля по отношению к доллару",
            "5. Fak5 - Деловая репутация разработчиков программного комплекса",
            "6. Fak6 - Деловая репутация эксплуатирующей организации",
        ]
        
        for desc in descriptions:
            self.listbox.insert(tk.END, desc)
        
        self.listbox.insert(tk.END, "")
        self.listbox.insert(tk.END, "Формулы возмущений:")
        for i, (formula, func) in self.disturbances.items():
            self.listbox.insert(tk.END, f"  {i}. {formula}")
        
        # График возмущений
        self._create_disturbance_plot()
    
    def _create_disturbance_plot(self):
        """Создать график всех возмущений."""
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        plot_frame = ttk.LabelFrame(self, text="Графики возмущений")
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        import numpy as np
        t = np.linspace(0, 1, 100)
        
        for i, (formula, func) in self.disturbances.items():
            values = [func(ti) for ti in t]
            ax.plot(t, values, label=f"Fak{i}")
        
        ax.set_xlabel("Время")
        ax.set_ylabel("Значение возмущения")
        ax.set_title("Динамика внешних возмущений")
        ax.legend()
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)