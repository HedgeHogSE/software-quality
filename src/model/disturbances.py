"""
Функции внешних возмущений (Fak1-Fak6).

Формат функций: f(t) -> значение возмущения в момент времени t.
Значения возмущений находятся в диапазоне [0, 1].
"""
import math


def fak1(t: float) -> float:
    """Fak1(t) = t^2 + 1"""
    return t * t + 1


def fak2(t: float) -> float:
    """
    Fak2(t) = cos(1.5*pi*t - pi/6)^2 / 4 + 0.2
    
    В документеdouble cos cos - это артефакт извлечения, на самом деле должно быть cos^2.
    """
    arg = 1.5 * math.pi * t - math.pi / 6
    return (math.cos(arg) ** 2) / 4 + 0.2


def fak3(t: float) -> float:
    """
    Fak3(t) = sin(sin(pi*t - pi/6)) / 2.5 + 0.3
    
    В документеdouble sin sin - это артефакт извлечения.
    Проверить: может быть имелось в виду sin^2 или sin(sin(...)).
    Используем синус от синуса как наиболее вероятную интерпретацию.
    """
    arg = math.pi * t - math.pi / 6
    return math.sin(math.sin(arg)) / 2.5 + 0.3


def fak4(t: float) -> float:
    """Fak4(t) = 2*t - 1"""
    return 2 * t - 1


def fak5(t: float) -> float:
    """
    Fak5(t) = sin(pi*t - pi/6)^2 / 2.5 + 0.3
    """
    arg = math.pi * t - math.pi / 6
    return (math.sin(arg) ** 2) / 2.5 + 0.3


def fak6(t: float) -> float:
    """
    Fak6(t) - гармоническая функция в диапазоне [0.3, 0.7].
    
    В документе не приведена явная формула для Fak6.
    Используем косинусоиду, сдвинутую в диапазон [0.3, 0.7].
    """
    arg = math.pi * t - math.pi / 6
    base = math.cos(arg) ** 2 / 4
    return base + 0.5  # центр диапазона [0.3, 0.7]


DISTURBANCES = {
    1: fak1,
    2: fak2,
    3: fak3,
    4: fak4,
    5: fak5,
    6: fak6,
}


def get_disturbance(n: int):
    """Получить функцию возмущения Fn по номеру."""
    return DISTURBANCES.get(n)