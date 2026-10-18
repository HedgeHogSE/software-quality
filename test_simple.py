"""Простой тест."""
import sys
sys.path.insert(0, 'src')

import time
import numpy as np
from model.equations import system
from model.parameters import get_initial_values

def test_system_function():
    """Проверка функции системы."""
    print("Тест функции системы...")
    
    system_impl = system
    u0 = get_initial_values(1)
    
    print(f"u0 = {u0[:3]}... (первые 3 значения)")
    
    t_test = 0.0
    try:
        result = system(t_test, u0)
        print(f"system({t_test}, u0) = {result[:3]}... (первые 3 значения)")
        print(f"Успешно вычислили систему! Длина результата: {len(result)}")
        return True
    except Exception as e:
        print(f"Ошибка при вызове системы: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system_function()
    if not success:
        print("Тест провален!")
        sys.exit(1)