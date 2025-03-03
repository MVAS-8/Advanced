import time
import threading
from concurrent.futures import ThreadPoolExecutor

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def compute_factorials(numbers):
    for num in numbers:
        factorial(num)

def measure_time_with_threads(numbers):
    threads = []
    start_time = time.time()
    
    for num in numbers:
        thread = threading.Thread(target=factorial, args=(num,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    return end_time - start_time

def measure_time_with_threadpool(numbers):
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(factorial, numbers)
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    numbers = [10000, 15000, 20000, 25000, 30000]
    
    time_threads = measure_time_with_threads(numbers)
    print(f"Час виконання з Threads: {time_threads:.4f} секунд")
    
    time_threadpool = measure_time_with_threadpool(numbers)
    print(f"Час виконання з ThreadPoolExecutor: {time_threadpool:.4f} секунд")