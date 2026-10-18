"""
Тесты моделирования.
"""
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from services.simulation_service import SimulationService
from model.parameters import get_initial_values


class TestSimulationService:
    """Тесты сервиса моделирования."""
    
    def test_run_simulation(self):
        """Проверка запуска симуляции."""
        service = SimulationService()
        result = service.run_simulation(implementation=1, t_end=0.1, step=0.01)
        
        assert result is not None
        assert result.success
        assert len(result.t) > 0
    
    def test_get_result(self):
        """Проверка получения результата."""
        service = SimulationService()
        service.run_simulation(implementation=1, t_end=0.1, step=0.01)
        
        result = service.get_result(1)
        assert result is not None
        assert result.success
    
    def test_get_control_points(self):
        """Проверка контрольных точек."""
        service = SimulationService()
        service.run_simulation(implementation=1, t_end=0.1, step=0.01)
        
        # Для короткого интервала 0-0.1 контрольные точки: 0.0, 0.025, 0.05, 0.075, 0.1
        control_points = service.get_control_points(1)
        
        assert len(control_points) >= 2
    
    def test_clear_results(self):
        """Проверка очистки результатов."""
        service = SimulationService()
        service.run_simulation(implementation=1, t_end=0.1, step=0.01)
        
        service.clear_results()
        
        assert len(service.get_all_results()) == 0