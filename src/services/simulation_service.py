"""
Сервис моделирования качества ПО.
"""
from typing import Dict, List, Optional
import numpy as np

from src.model.parameters import PARAMETERS, get_initial_values
from src.model.solver import solve_system, SimulationResult


class SimulationService:
    """Сервис управления симуляциями."""
    
    def __init__(self):
        self._results: Dict[int, SimulationResult] = {}
    
    def run_simulation(self, implementation: int = 1, **kwargs) -> SimulationResult:
        """
        Запустить симуляцию для указанной реализации.
        
        Args:
            implementation: номер реализации (1-5)
            **kwargs: параметры решателя (t_start, t_end, step и т.д.)
        
        Returns:
            Результат симуляции
        """
        result = solve_system(implementation, **kwargs)
        self._results[implementation] = result
        return result
    
    def get_result(self, implementation: int) -> Optional[SimulationResult]:
        """Получить результат для реализации (если уже запущена)."""
        return self._results.get(implementation)
    
    def get_all_results(self) -> Dict[int, SimulationResult]:
        """Получить все результаты симуляций."""
        return self._results.copy()
    
    def get_control_points(self, implementation: int) -> Dict[int, List[float]]:
        """
        Получить состояния системы в пяти контрольных точках.
        
        Returns:
            {0: state_at_t0, 25: state_at_t0.25, 50: state_at_t0.5, ...}
        """
        if implementation not in self._results:
            self.run_simulation(implementation)
        
        result = self._results[implementation]
        if not result.success:
            return {}
        
        # Динамическое вычисление индексов контрольных точек
        n = len(result.t)
        control_indices = [0, max(1, n//4), max(1, n//2), max(1, 3*n//4), n-1]
        
        return {
            idx: result.get_state_at_time(idx) for idx in control_indices
        }
    
    def clear_results(self):
        """Очистить все сохранённые результаты."""
        self._results.clear()