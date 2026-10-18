"""
Тесты функций модели.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.functions import linear_func, quadratic_func, cubic_func, FUNCTIONS


class TestLinearFunc:
    """Тесты линейной функции f(x) = a*x + b."""
    
    def test_linear_default(self):
        """Тест по умолчанию f(x) = x."""
        result = linear_func(5.0)
        assert result == 5.0
    
    def test_linear_with_params(self):
        """Тест с заданными параметрами."""
        result = linear_func(2.0, a=3.0, b=1.0)
        assert result == 7.0  # 3*2 + 1 = 7
    
    def test_linear_negative(self):
        """Тест с отрицательными значениями."""
        result = linear_func(-2.0, a=2.0, b=3.0)
        assert result == -1.0  # 2*(-2) + 3 = -1


class TestQuadraticFunc:
    """Тесты квадратичной функции f(x) = a*x^2 + b*x + c."""
    
    def test_quadratic_default(self):
        """Тест по умолчанию f(x) = x^2 (a=1, остальные 0)."""
        result = quadratic_func(3.0)
        assert result == 9.0  # 1*9 + 0*3 + 0 = 9
    
    def test_quadratic_with_params(self):
        """Тест с заданными параметрами."""
        result = quadratic_func(2.0, a=1.0, b=1.0, c=1.0)
        assert result == 7.0  # 1*4 + 1*2 + 1 = 7
    
    def test_quadratic_negative(self):
        """Тест с отрицательными значениями."""
        result = quadratic_func(-1.0, a=1.0, b=0.0, c=0.0)
        assert result == 1.0  # 1*1 = 1


class TestCubicFunc:
    """Тесты кубической функции f(x) = a*x^3 + b*x^2 + c*x + d."""
    
    def test_cubic_default(self):
        """Тест по умолчанию f(x) = x^3 (a=1, остальные 0)."""
        result = cubic_func(2.0)
        assert result == 8.0  # 1*8 = 8
    
    def test_cubic_with_params(self):
        """Тест с заданными параметрами."""
        result = cubic_func(2.0, a=1.0, b=0.0, c=0.0, d=0.0)
        assert result == 8.0  # 1*8 = 8
    
    def test_cubic_complex(self):
        """Тест сложного выражения."""
        result = cubic_func(2.0, a=0.2, b=0.8, c=0.2, d=0.09)
        expected = 0.2*8 + 0.8*4 + 0.2*2 + 0.09
        assert abs(result - expected) < 1e-10


class TestFunctionRegistry:
    """Тесты реестра функций."""
    
    def test_get_function_linear(self):
        """Получить линейную функцию."""
        func = FUNCTIONS.get_function(5)
        result = func(2.0)
        assert abs(result - 1.0) < 1e-10  # a=1, b=0 => f(2) = 2
    
    def test_get_function_quadratic(self):
        """Получить квадратичную функцию."""
        func = FUNCTIONS.get_function(9)
        result = func(2.0)
        expected = 0.7 * 4 - 0.4 * 2 + 0.24
        assert abs(result - expected) < 1e-10
    
    def test_get_function_cubic(self):
        """Получить кубическую функцию."""
        func = FUNCTIONS.get_function(3)
        result = func(2.0)
        expected = 0.2 * 8 + 0.8 * 4 + 0.2 * 2 + 0.09
        assert abs(result - expected) < 1e-10
    
    def test_function_out_of_range(self):
        """Тест выхода за пределы диапазона."""
        with pytest.raises(ValueError):
            FUNCTIONS.get_function(0)
        with pytest.raises(ValueError):
            FUNCTIONS.get_function(188)