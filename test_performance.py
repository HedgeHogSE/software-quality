"""Тест производительности решателя."""
import sys
sys.path.insert(0, 'src')

import time
from model.solver import solve_system
from model.parameters import get_initial_values

def test_basic_solver():
    """Простой тест решателя."""
    print("=== Тест 1: Базовое решение (implementation=1, step=0.01) ===")
    
    start = time.time()
    result = solve_system(implementation=1, step=0.01)
    elapsed = time.time() - start
    
    print(f"Время выполнения: {elapsed:.3f} сек")
    print(f"Успех: {result.success}")
    print(f"Сообщение: {result.message}")
    print(f"Точек: {len(result.t)}")
    print(f"u5[0] = {result.get_value_at_time(0, 0):.6f}")
    print(f"u5[100] = {result.get_value_at_time(100, 0):.6f}")
    
    return result.success and elapsed < 60

def test_small_step():
    """Тест с меньшим шагом."""
    print("\n=== Тест 2: Меньший шаг (step=0.005) ===")
    
    start = time.time()
    result = solve_system(implementation=1, step=0.005)
    elapsed = time.time() - start
    
    print(f"Время выполнения: {elapsed:.3f} сек")
    print(f"Успех: {result.success}")
    print(f"Точек: {len(result.t)}")
    
    return result.success and elapsed < 60

def test_implementation(impl: int):
    """Тест конкретной реализации."""
    print(f"\n=== Тест 3: Реализация {impl} ===")
    
    start = time.time()
    result = solve_system(implementation=impl, step=0.01)
    elapsed = time.time() - start
    
    print(f"Время выполнения: {elapsed:.3f} сек")
    print(f"Успех: {result.success}")
    print(f"Сообщение: {result.message}")
    
    return result.success

def test_stiff_solver():
    """Тест с жёстким решателем Radau."""
    print("\n=== Тест 4: Жёсткий решатель (method='Radau') ===")
    
    start = time.time()
    result = solve_system(implementation=1, step=0.01, method='Radau')
    elapsed = time.time() - start
    
    print(f"Время выполнения: {elapsed:.3f} сек")
    print(f"Успех: {result.success}")
    print(f"Сообщение: {result.message}")
    
    return result.success

if __name__ == "__main__":
    print("Тестирование решателя системы ДУ...")
    
    results = []
    results.append(("Базовое решение", test_basic_solver()))
    results.append(("Меньший шаг", test_small_step()))
    
    for impl in [2, 3]:
        results.append((f"Реализация {impl}", test_implementation(impl)))
    
    results.append(("Жёсткий решатель", test_stiff_solver()))
    
    print("\n=== Сводка ===")
    for name, success in results:
        status = "✓ УСПЕХ" if success else "✗ ПРОВАЛ"
        print(f"{status}: {name}")