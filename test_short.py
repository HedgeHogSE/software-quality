"""Простой тест с уменьшенным шагом."""
import sys
sys.path.insert(0, 'src')

import time
from model.solver import solve_system

def test_with_small_step():
    """Тест с уменьшенным интервалом и шагом."""
    print("Тест с уменьшенным интервалом [0, 0.1] и шагом 0.01...")
    
    start = time.time()
    result = solve_system(implementation=1, t_end=0.1, step=0.01)
    elapsed = time.time() - start
    
    print(f"Время выполнения: {elapsed:.3f} сек")
    print(f"Успех: {result.success}")
    print(f"Сообщение: {result.message}")
    print(f"Точек: {len(result.t)}")
    
    return result.success

if __name__ == "__main__":
    success = test_with_small_step()
    print(f"\nРезультат: {'УСПЕХ' if success else 'ПРОВАЛ'}")