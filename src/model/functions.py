"""
Функции модели (f1-f187).

Типы функций:
- Линейная: f(x) = a*x + b
- Квадратичная: f(x) = a*x^2 + b*x + c
- Кубическая: f(x) = a*x^3 + b*x^2 + c*x + d

Для функций без явного определения в документе используется стандартная линейная аппроксимация f(x) = x.
"""
from typing import Callable


def linear_func(x: float, a: float = 1.0, b: float = 0.0) -> float:
    """Линейная функция: f(x) = a*x + b"""
    return a * x + b


def quadratic_func(x: float, a: float = 1.0, b: float = 0.0, c: float = 0.0) -> float:
    """Квадратичная функция: f(x) = a*x^2 + b*x + c"""
    return a * x * x + b * x + c


def cubic_func(x: float, a: float = 1.0, b: float = 0.0, c: float = 0.0, d: float = 0.0) -> float:
    """Кубическая функция: f(x) = a*x^3 + b*x^2 + c*x + d"""
    return a * x * x * x + b * x * x + c * x + d


class FunctionRegistry:
    """
    Реестр функций f1-f187.
    
    Для каждой функции указан тип и коэффициенты.
    По умолчанию используется f(x) = x (a=1, остальные 0).
    """
    
    def __init__(self):
        self._functions = {}
        self._setup_functions()
    
    def _setup_functions(self):
        """Настройка функций на основе данных из документа."""
        
        # Известные функции из документа (Рис. 3, 5)
        self._functions[3] = ('cubic', 0.2, 0.8, 0.2, 0.09)
        self._functions[5] = ('linear', 0.25, 0.5, 0.0, 0.0)
        self._functions[9] = ('quadratic', 0.7, -0.4, 0.24, 0.0)
        self._functions[48] = ('linear', 0.53, 0.17, 0.0, 0.0)
        self._functions[72] = ('quadratic', 0.5, 0.27, 0.9, 0.0)
        self._functions[81] = ('linear', 0.28, -0.63, 0.0, 0.0)
        self._functions[117] = ('quadratic', 0.72, 0.12, 0.8, 0.0)
        
        # Остальные функции по умолчанию: f(x) = x
        for i in range(1, 188):
            if i not in self._functions:
                self._functions[i] = ('linear', 1.0, 0.0, 0.0, 0.0)
    
    def get_function(self, n: int) -> Callable[[float], float]:
        """
        Получить функцию fn по её номеру.
        
        Returns:
            Функцию, вычисляющую fn(x)
        """
        if n < 1 or n > 187:
            raise ValueError(f"Function f{n} does not exist. Must be in range [1, 187]")
        
        func_type, a, b, c, d = self._functions[n]
        
        if func_type == 'linear':
            return linear_func if (a == 1.0 and b == 0.0) else lambda x: linear_func(x, a, b)
        elif func_type == 'quadratic':
            return quadratic_func if (a == 1.0 and b == 0.0 and c == 0.0) else lambda x: quadratic_func(x, a, b, c)
        elif func_type == 'cubic':
            return cubic_func if (a == 1.0 and b == 0.0 and c == 0.0 and d == 0.0) else lambda x: cubic_func(x, a, b, c, d)
        else:
            return linear_func
    
    def get_all_functions(self) -> dict:
        """Получить все функции в виде словаря."""
        return {i: self.get_function(i) for i in range(1, 188)}


# Глобальный реестр функций
FUNCTIONS = FunctionRegistry()