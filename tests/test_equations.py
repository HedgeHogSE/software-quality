"""
Тесты уравнений модели.
"""
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.equations import (
    get_system_function, equation_u5, equation_u24, EQUATIONS
)
from model.disturbances import fak1, fak2, fak3, fak4, fak5, fak6


class TestEquationSystem:
    """Тесты системы уравнений."""
    
    def test_system_returns_28_equations(self):
        """Проверка количества уравнений."""
        system = get_system_function()
        
        # Создать тестовый вектор состояния
        u = np.ones(28).tolist()
        t = 0.0
        
        result = system(t, u, {})
        
        assert len(result) == 28
    
    def test_system_dimensions_match(self):
        """Проверка соответствия размеров."""
        system = get_system_function()
        
        u = np.random.rand(28).tolist()
        t = 0.5
        
        result = system(t, u, {})
        
        assert len(result) == len(u)
    
    def test_equation_u5_structure(self):
        """Проверка структуры уравнения для u5."""
        u = [0.65, 0.7, 0.6, 0.6, 0.7, 0.4, 0.78, 0.24, 0.56,
             0.23, 0.52, 0.25, 0.67, 0.72, 0.67, 0.3, 0.4, 0.6,
             0.23, 0.42, 0.56, 0.67, 0.45, 0.54, 0.67, 0.0, 0.0, 0.0]
        
        result = equation_u5(0.0, u, {})
        
        # Результат должен быть числом
        assert isinstance(result, (int, float))
        assert not np.isnan(result)
        assert not np.isinf(result)


class TestDisturbanceValues:
    """Тесты значений возмущений."""
    
    def test_fak1_values(self):
        """Проверка значений Fak1."""
        assert fak1(0.0) == 1.0
        assert fak1(0.5) == 1.25
        assert fak1(1.0) == 2.0
    
    def test_fak4_values(self):
        """Проверка значений Fak4."""
        assert fak4(0.0) == -1.0
        assert fak4(0.5) == 0.0
        assert fak4(1.0) == 1.0