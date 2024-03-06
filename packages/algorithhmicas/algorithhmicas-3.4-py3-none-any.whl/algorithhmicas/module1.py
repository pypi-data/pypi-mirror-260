def main_function():
    print("Hello my friend")

def factorial(n):
    """Вычисляет факториал числа n.)"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Этот код будет выполнен только при запуске файла напрямую, а не при импортировании из другого файла.
if __name__ == "__main__":
    print("Пример использования модуля module1.py:)")
    print("Факториал числа 5:", factorial(5))
