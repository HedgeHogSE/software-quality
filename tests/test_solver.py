"""
Тесты численного решателя.
"""
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.solver import solve_system, SimulationResult


class TestSolver:
    """Тесты численного решателя."""
    
    def test_solve_returns_result(self):
        """Проверка возвращаемого результата."""
        result = solve_system(implementation=1, t_end=0.1, step=0.01)
        
        assert isinstance(result, SimulationResult)
        assert result.success
    
    def test_solve_has_time_array(self):
        """Проверка массива времени."""
        result = solve_system(implementation=1, t_end=0.1, step=0.01)
        
        assert len(result.t) > 0
        assert result.t[0] == 0.0
        assert result.t[-1] == 0.1
    
    def test_solve_has_state_array(self):
        """Проверка массива состояний."""
        result = solve_system(implementation=1, t_end=0.1, step=0.01)
        
        assert result.u.shape[0] == 28
        assert result.u.shape[1] > 0
    
    def test_solve_dimensions_match(self):
        """Проверка соответствия размеров времени и состояния."""
        result = solve_system(implementation=1, t_end=0.1, step=0.01)
        
        assert len(result.t) == result.u.shape[1]
    
    def test_solve_values_are_finite(self):
        """Проверка конечности значений."""
        result = solve_system(implementation=1, t_end=0.1, step=0.01)
        
        assert np.all(np.isfinite(result.u))
    
    def test_multiple_implementations(self):
        """Проверка нескольких реализаций."""
        for impl in range(1, 6):
            result = solve_system(implementation=impl, t_end=0.1, step=0.01)
            assert result.success
            assert result.u.shape[0] == 28


class TestControlPoints:
    """Тесты контрольных точек."""
    
    def test_control_points_calculation(self):
        """Проверка расчёта контрольных точек."""
        result = solve_system(implementation=1, t_end=0.1, step=0.01)
        
        # Проверка промежуточных значений
        state = result.get_state_at_time(5)
        assert len(state) == 28
        assert all(np.isfinite(v) for v in state)