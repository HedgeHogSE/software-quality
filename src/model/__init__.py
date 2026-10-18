"""
Пакет математической модели.

Модули:
- functions.py: функции f1-f187 (линейные, квадратичные, кубические)
- disturbances.py: функции возмущений Fak1-Fak6
- parameters.py: коэффициенты и начальные значения
- equations.py: 28 дифференциальных уравнений
- solver.py: численное решение системы
"""
from .functions import FUNCTIONS
from .disturbances import DISTURBANCES
from .parameters import PARAMETERS, get_initial_values
from .equations import EQUATIONS, system
from .solver import solve_system, SimulationResult