import time
import random
import sys
import tracemalloc
import matplotlib.pyplot as plt

# Increase recursion limit for deep recursions in Quick Sort
sys.setrecursionlimit(10000)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def generate_datasets(size):
    """Generate sorted, reverse sorted, and random datasets."""
    sorted_data = list(range(size))
    reverse_sorted_data = sorted_data[::-1]
    random_data = random.sample(range(size * 10), size)
    return sorted_data, reverse_sorted_data, random_data

def measure_performance(sort_function, data):
    """Measure the execution time and memory usage of the sorting function."""
    tracemalloc.start()  # Start memory tracking
    start_time = time.time()  # Start time tracking
    
    sort_function(data)
    
    end_time = time.time()  # End time tracking
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop memory tracking
    
    exec_time = end_time - start_time  # Execution time
    memory_usage = peak / 1024  # Memory usage in KB
    return exec_time, memory_usage

if __name__ == "__main__":
    sizes = [1000, 5000, 10000, 20000]  # Dataset sizes
    sort_functions = [quick_sort, merge_sort]
    dataset_types = ["sorted", "reverse sorted", "random"]

    # Dictionaries to store performance data
    performance_data = {func.__name__: {dtype: {'time': [], 'memory': []} for dtype in dataset_types} for func in sort_functions}

    for size in sizes:
        sorted_data, reverse_sorted_data, random_data = generate_datasets(size)
        datasets = {"sorted": sorted_data, "reverse sorted": reverse_sorted_data, "random": random_data}

        for sort_function in sort_functions:
            for dtype, data in datasets.items():
                exec_time, memory_usage = measure_performance(sort_function, data[:])
                performance_data[sort_function.__name__][dtype]['time'].append(exec_time)
                performance_data[sort_function.__name__][dtype]['memory'].append(memory_usage)
                print(f"{sort_function.__name__} on {dtype} data of size {size} took {exec_time:.5f} seconds and used {memory_usage:.2f} KB of memory.")

    # Plotting the results for execution time
    for dtype in dataset_types:
        plt.figure(figsize=(10, 6))
        for sort_function in sort_functions:
            plt.plot(sizes, performance_data[sort_function.__name__][dtype]['time'], label=sort_function.__name__)
        
        plt.title(f"Execution Time of Sorting Algorithms on {dtype.capitalize()} Data")
        plt.xlabel("Dataset Size")
        plt.ylabel("Execution Time (seconds)")
        plt.legend()
        plt.grid(True)
        
        # Save the graph as a .png file
        filename = f"execution_time_{dtype}_data.png"
        plt.savefig(filename)
        print(f"Execution time graph saved as {filename}")
        plt.close()  # Close the plot to prevent overwriting

    # Plotting the results for memory usage
    for dtype in dataset_types:
        plt.figure(figsize=(10, 6))
        for sort_function in sort_functions:
            plt.plot(sizes, performance_data[sort_function.__name__][dtype]['memory'], label=sort_function.__name__)
        
        plt.title(f"Memory Usage of Sorting Algorithms on {dtype.capitalize()} Data")
        plt.xlabel("Dataset Size")
        plt.ylabel("Memory Usage (KB)")
        plt.legend()
        plt.grid(True)
        
        # Save the graph as a .png file
        filename = f"memory_usage_{dtype}_data.png"
        plt.savefig(filename)
        print(f"Memory usage graph saved as {filename}")
        plt.close()  # Close the plot to prevent overwriting

