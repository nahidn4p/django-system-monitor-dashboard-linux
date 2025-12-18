import os
import time
import random
import threading
import multiprocessing


def cpu_intensive_task(duration, intensity):
    """CPU intensive task that runs for a specified duration"""
    end_time = time.time() + duration
    while time.time() < end_time:
        # Perform CPU-intensive calculations
        result = sum(i * i for i in range(int(intensity * 1000)))
        time.sleep(0.001)  # Small sleep to prevent complete lockup


def memory_intensive_task(duration, memory_mb):
    """Memory intensive task that allocates memory"""
    try:
        # Allocate memory (in MB)
        data = bytearray(memory_mb * 1024 * 1024)
        # Keep it in memory for the duration
        time.sleep(duration)
        # Memory will be freed when function exits
    except MemoryError:
        pass


def spike_cpu_ram():
    """
    Scheduled task to spike CPU and RAM usage
    Randomly spikes between 30-50% of available resources
    """
    import psutil
    
    # Get system resources
    cpu_count = psutil.cpu_count()
    memory = psutil.virtual_memory()
    
    # Random intensity between 30-50%
    cpu_intensity = random.uniform(0.30, 0.50)
    ram_intensity = random.uniform(0.30, 0.50)
    
    # Calculate target usage
    target_cpu_cores = max(1, int(cpu_count * cpu_intensity))
    target_memory_mb = int((memory.total / (1024 * 1024)) * ram_intensity)
    
    # Duration: random between 5-15 minutes
    duration = random.randint(300, 900)  # 5-15 minutes in seconds
    
    print(f"Spiking CPU ({target_cpu_cores} cores) and RAM ({target_memory_mb} MB) for {duration} seconds")
    
    # Start CPU intensive tasks
    cpu_threads = []
    for _ in range(target_cpu_cores):
        thread = threading.Thread(
            target=cpu_intensive_task,
            args=(duration, cpu_intensity),
            daemon=True
        )
        thread.start()
        cpu_threads.append(thread)
    
    # Start memory intensive tasks
    memory_threads = []
    # Split memory across multiple threads
    memory_per_thread = max(100, target_memory_mb // 4)  # At least 100MB per thread
    num_memory_threads = min(4, max(1, target_memory_mb // memory_per_thread))
    
    for _ in range(num_memory_threads):
        thread = threading.Thread(
            target=memory_intensive_task,
            args=(duration, memory_per_thread),
            daemon=True
        )
        thread.start()
        memory_threads.append(thread)
    
    # Wait for all threads to complete
    for thread in cpu_threads + memory_threads:
        thread.join(timeout=duration + 10)
    
    print("CPU/RAM spike task completed")

