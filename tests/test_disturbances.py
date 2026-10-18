"""
Тесты функций возмущений.
"""
import pytest
import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.disturbances import fak1, fak2, fak3, fak4, fak5, fak6


class TestFak1:
    """Тесты Fak1(t) = t^2 + 1."""
    
    def test_at_zero(self):
        """Значение в t=0."""
        assert fak1(0.0) == 1.0
    
    def test_at_one(self):
        """Значение в t=1."""
        assert fak1(1.0) == 2.0
    
    def test_at_half(self):
        """Значение в t=0.5."""
        assert fak1(0.5) == 1.25


class TestFak2:
    """Тесты Fak2(t) = cos^2(1.5*pi*t - pi/6) / 4 + 0.2."""
    
    def test_at_zero(self):
        """Значение в t=0."""
        arg = -math.pi / 6
        expected = (math.cos(arg) ** 2) / 4 + 0.2
        assert abs(fak2(0.0) - expected) < 1e-10
    
    def test_at_one(self):
        """Значение в t=1."""
        arg = 1.5 * math.pi - math.pi / 6
        expected = (math.cos(arg) ** 2) / 4 + 0.2
        assert abs(fak2(1.0) - expected) < 1e-10


class TestFak3:
    """Тесты Fak3(t) = sin(sin(pi*t - pi/6)) / 2.5 + 0.3."""
    
    def test_at_zero(self):
        """Значение в t=0."""
        arg = -math.pi / 6
        expected = math.sin(math.sin(arg)) / 2.5 + 0.3
        assert abs(fak3(0.0) - expected) < 1e-10
    
    def test_at_one(self):
        """Значение в t=1."""
        arg = math.pi - math.pi / 6
        expected = math.sin(math.sin(arg)) / 2.5 + 0.3
        assert abs(fak3(1.0) - expected) < 1e-10


class TestFak4:
    """Тесты Fak4(t) = 2t - 1."""
    
    def test_at_zero(self):
        """Значение в t=0."""
        assert fak4(0.0) == -1.0
    
    def test_at_half(self):
        """Значение в t=0.5."""
        assert fak4(0.5) == 0.0
    
    def test_at_one(self):
        """Значение в t=1."""
        assert fak4(1.0) == 1.0


class TestFak5:
    """Тесты Fak5(t) = sin^2(pi*t - pi/6) / 2.5 + 0.3."""
    
    def test_at_zero(self):
        """Значение в t=0."""
        arg = -math.pi / 6
        expected = (math.sin(arg) ** 2) / 2.5 + 0.3
        assert abs(fak5(0.0) - expected) < 1e-10
    
    def test_at_one(self):
        """Значение в t=1."""
        arg = math.pi - math.pi / 6
        expected = (math.sin(arg) ** 2) / 2.5 + 0.3
        assert abs(fak5(1.0) - expected) < 1e-10


class TestFak6:
    """Тесты Fak6(t) - гармоническая функция [0.3, 0.7]."""
    
    def test_range(self):
        """Проверка диапазона значений."""
        import numpy as np
        t_values = np.linspace(0, 1, 100)
        values = [fak6(t) for t in t_values]
        
        # Простая проверка: значение должно быть числом
        assert all(isinstance(v, (int, float)) for v in values)
        assert any(0.3 <= v <= 0.7 for v in values)
    
    def test_at_zero(self):
        """Значение в t=0."""
        result = fak6(0.0)
        assert 0.3 <= result <= 0.7