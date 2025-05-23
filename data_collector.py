"""
data_collector.py

Esse módulo apresenta as funções de leitura e cálculo dos dados do SO a partir do diretório /proc/ em sistemas Linux.
"""

import os
import time
import pwd

"""
Lê os dados da CPU a partir do arquivo /proc/stat.

Returns:
    list: Inteiros.
"""
def cpu_file_reader():
    with open("/proc/stat", "r") as file:
        cpu_time = (file.readline()).split()[1:]
    return list(map(int, cpu_time))


"""
Lê todos os dados sobre a memória a partir do arquivo /proc/meminfo.

Returns:
    memory_info: (key, data), String e inteiro respectivamente.
"""
def memory_file_reader():
    memory_info = {}

    with open("/proc/meminfo", "r") as file:
        for line in file:
            key, value = line.split(":")
            memory_info[key.strip()] = int(value.strip().split()[0])

    return memory_info


"""
Lê informações estáticas da CPU a partir do arquivo /proc/cpuinfo.

Returns:
    cpu_model_name: String com dados do modelo da cpu.
"""
def cpu_data_collector():
    with open("/proc/cpuinfo", "r") as file:
        cpu_model_name = file.readlines()[4].split()[3:]

    return cpu_model_name


"""
Filtra informações estáticas da memória.

Returns:
    memory_data_processed: (type, data), String e inteiro respectivamente.
"""
def memory_data_collector():
    memory_data_processed = {}
    memory_info = memory_file_reader()

    # Separa informações úteis do dicionário inial
    total_memory = memory_info["MemTotal"]
    total_swap = memory_info["SwapTotal"]
    total_vmem = total_memory + total_swap

    # Adiciona as informações no dicionário final
    memory_data_processed["total_memory"] = total_memory
    memory_data_processed["total_swap"] = total_swap
    memory_data_processed["total_vmem"] = total_vmem

    return memory_data_processed


"""
Trata informações dinâmicas da CPU, como porcentagem de uso e tempo ocioso.

Returns:
    cpu_percent_processed: (type, percent), String e float respectivamente.
"""
def cpu_percent_collector():
    cpu_percent_processed = {}

    # Busca informações da CPU com delay de um segundo
    time_init = cpu_file_reader()
    time.sleep(0.5)
    time_end = cpu_file_reader()

    # Tempo ocioso
    idle_init = time_init[3] + time_init[4]
    idle_end = time_end[3] + time_end[4]

    # Uso total
    total_init = sum(time_init)
    total_end = sum(time_end)

    # Diferença entre o ponto inicial e o final
    total_diff = total_end - total_init
    idle_diff = idle_end - idle_init

    # Porcentagens
    cpu_usage_percent = (1 - idle_diff / total_diff) * 100
    cpu_idle_percent = (idle_diff / total_diff) * 100

    # Dicionário com as porcentagens de uso da CPU
    cpu_percent_processed["cpu_usage_percent"] = round(cpu_usage_percent, 1)
    cpu_percent_processed["cpu_idle_percent"] = round(cpu_idle_percent, 1)

    return cpu_percent_processed


"""
Trata informações dinâmicas da memória, como memória usada, memória virtual usada, etc.

Returns:
    memory_percent_processed: (type, percent), String e float respectivamente.
"""
def memory_percent_collector():
    memory_percent_processed = {}
    memory_info = memory_file_reader()

    # Memória física
    total_memory = memory_info["MemTotal"]
    free_memory = (memory_info["MemFree"] + memory_info["Buffers"] + memory_info["Cached"])
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

    # Dicionário com as porcentagens de uso das memórias
    memory_percent_processed["memory_usage_percent"] = round(memory_usage_percent, 1)
    memory_percent_processed["memory_free_percent"] = round(memory_free_percent, 1)
    memory_percent_processed["vmem_usage_percent"] = round(vmem_usage_percent, 1)
    memory_percent_processed["vmem_free_percent"] = round(vmem_free_percent, 1)

    return memory_percent_processed


"""
Conta o número de processos em andamento a partir do diretório /proc/.

Returns:
    sum: Somatório do número de processos.
"""
def process_count():
    return sum(1 for name in os.listdir("/proc/") if name.isdigit())

"""
Registra os processos com seus respectivos ID, nome e usuário

Returns:
    processes: Lista onde cada item é uma tupla com: (process_id, process_name, user)
"""
def processes_with_users():
    processes = []

    for process_id in os.listdir("/proc"):
        if process_id.isdigit():
            status_path = os.path.join("/proc", process_id, "status")
            with open(status_path, "r") as file:
                lines = file.readlines()
                user_id_line = next(line for line in lines if line.startswith("Uid:"))
                user_id = int(user_id_line.split()[1])  # UID real
                user = pwd.getpwuid(user_id).pw_name

                name_line = next(line for line in lines if line.startswith("Name:"))
                proces_name = name_line.split()[1]

                processes.append((process_id, proces_name, user))

    return processes
