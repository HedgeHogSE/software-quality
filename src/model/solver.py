"""
Численное решение системы дифференциальных уравнений.

Использует scipy.integrate.solve_ivp с методом Рунге-Кутты.
"""
from typing import List, Tuple, Dict, Optional
import numpy as np
from scipy.integrate import solve_ivp

from .equations import system, EQUATIONS
from .parameters import PARAMETERS, get_initial_values


class SimulationResult:
    """Результат симуляции."""
    
    def __init__(self, t: np.ndarray, u: np.ndarray, success: bool, message: str = ""):
        self.t = t
        self.u = u
        self.success = success
        self.message = message
    
    def get_variable(self, index: int) -> np.ndarray:
        """Получить значения переменной по её индексу."""
        if index < 0 or index >= self.u.shape[0]:
            raise IndexError(f"Variable index {index} out of range [0, {self.u.shape[0]})")
        return self.u[index, :]
    
    def get_value_at_time(self, t_index: int, var_index: int) -> float:
        """Получить значение переменной в конкретный момент времени."""
        return self.u[var_index, t_index]
    
    def get_state_at_time(self, t_index: int) -> List[float]:
        """Получить состояние системы (все переменные) в конкретный момент времени."""
        return self.u[:, t_index].tolist()


def solve_system(
    implementation: int = 1,
    t_start: float = None,
    t_end: float = None,
    step: float = None,
    rtol: float = 1e-3,
    atol: float = 1e-3,
    method: str = 'Radau'
) -> SimulationResult:
    """
    Решить систему дифференциальных уравнений для указанной реализации.
    
    Args:
        implementation: номер реализации (1-5)
        t_start: начало интервала времени
        t_end: конец интервала времени
        step: шаг вывода результатов
        rtol: относительная точность (уменьшена для скорости)
        atol: абсолютная точность (уменьшена для скорости)
        method: метод интегрирования ('RK45', 'Radau', 'BDF')
    
    Returns:
        SimulationResult с результатами моделирования
    """
    if t_start is None:
        t_start = PARAMETERS.t_start
    if t_end is None:
        t_end = PARAMETERS.t_end
    if step is None:
        step = PARAMETERS.step
    
    # Начальные условия
    u0 = get_initial_values(implementation)
    
    # Создать массив точек вывода
    n_points = max(101, int((t_end - t_start) / (step if step and step > 0 else 0.01)) + 1)
    t_eval = np.linspace(t_start, t_end, n_points)
    
    # Получить функцию системы
    system_impl = system
    
    # Решить систему
    try:
        sol = solve_ivp(
            fun=system,
            t_span=(t_start, t_end),
            y0=u0,
            t_eval=t_eval,
            method=method,
            rtol=rtol,
            atol=atol,
            vectorized=False,
            max_step=step if step and step > 0 else 0.1,
            events=None
        )
        
        if sol.success:
            return SimulationResult(
                t=sol.t,
                u=sol.y,
                success=True,
                message="Success"
            )
        else:
            return SimulationResult(
                t=sol.t,
                u=sol.y,
                success=False,
                message=sol.message
            )
    
    except Exception as e:
        return SimulationResult(
            t=np.array([]),
            u=np.array([]),
            success=False,
            message=str(e)
        )


def solve_for_control_points(implementation: int = 1) -> Dict[int, List[float]]:
    """
    Решить систему и получить состояния в пяти контрольных точках:
    0, 0.25, 0.5, 0.75, 1.0
    
    Returns:
        Словарь {t_index: state_vector}
    """
    result = solve_system(implementation)
    
    if not result.success:
        return {}
    
    # Индексы контрольных точек для step=0.01 на интервале [0,1]
    control_indices = [0, 25, 50, 75, 100]
    
    return {
        idx: result.get_state_at_time(idx) for idx in control_indices
    }