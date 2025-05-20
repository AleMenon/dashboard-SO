"""
def read_cpu_times():
    with open("/proc/stat", "r") as file:
        cpu_time = (file.readline()).split()[1:]
    return list(map(int, cpu_time))


def cpu_usage():
    time_init = read_cpu_times()
    time.sleep(1)
    time_end = read_cpu_times()

    idle_init = time_init[3] + time_init[4]
    idle_end = time_end[3] + time_end[4]

    total_init = sum(time_init)
    total_end = sum(time_end)

    total_diff = total_end - total_init
    idle_diff = idle_end - idle_init

    cpu_usage = (1 - idle_diff / total_diff) * 100

    return round(cpu_usage, 2)


def cpu_data_collector():
    with open("/proc/cpuinfo", "r") as file:
        cpu_model_name = file.readlines()[4].split()[3:]

    cpu_usage_percent = cpu_usage()

    return cpu_model_name, cpu_usage_percent
"""


def memory_data_collector():
    # Declaração dos dicionários
    memory_info = {}
    memory_data_processed = {}
    memory_percent_processed = {}

    # Manuseio do arquivo meminfo
    with open("/proc/meminfo", "r") as file:
        for line in file:
            key, value = line.split(":")
            memory_info[key.strip()] = int(value.strip().split()[0])

    # Memória física
    total_memory = memory_info["MemTotal"]
    free_memory = (
        memory_info["MemFree"] + memory_info["Buffers"] + memory_info["Cached"]
    )
    used_memory = total_memory - free_memory

    # Memória swap
    total_swap = memory_info["SwapTotal"]
    free_swap = memory_info["SwapFree"]
    used_swap = total_swap - free_swap

    # Memória virtual = RAM + Swap
    total_vmem = total_memory + total_swap
    used_vmem = used_memory + used_swap

    # Porcentagens
    memory_usage_percent = (used_memory / total_memory) * 100
    memory_free_percent = 100 - memory_usage_percent

    vmem_usage_percent = (used_vmem / total_vmem) * 100 if total_vmem > 0 else 0
    vmem_free_percent = 100 - vmem_usage_percent

    # Dicionário com as quantidades de cada memória
    memory_data_processed["total_memory"] = total_memory
    memory_data_processed["total_swap"] = total_swap
    memory_data_processed["total_vmem"] = total_vmem

    # Dicionário com as porcentagens de uso das memórias
    memory_percent_processed["memory_usage_percent"] = memory_usage_percent
    memory_percent_processed["memory_free_percent"] = memory_free_percent
    memory_percent_processed["vmem_usage_percent"] = vmem_usage_percent
    memory_percent_processed["vmem_free_percent"] = vmem_free_percent

    return memory_data_processed, memory_percent_processed


"""
def processes_data_collector():
    path="/proc/"

    for directory in os.listdir(path):
        if directory.isdigit:
            process_directory=os.path.join(path, directory)

            try:
                with open(os.path.join(process_directory, "status")) as file:


"""
