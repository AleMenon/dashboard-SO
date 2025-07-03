"""
data_collector.py

Esse módulo apresenta a classe DataCollector que implementa métodos para leitura e cálculo dos dados do SO a partir do diretório /proc/ 
em sistemas Linux.
"""

import ctypes
import ctypes.util
import time
from pathlib import Path
from file_system_collector import Statvfs

class DataCollector:
    # Construtor
    def __init__(self):
        # Carrega libc e statvfs
        self.libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno = True)
        self.statvfs = self.libc.statvfs
        self.statvfs.argtypes = [ctypes.c_char_p, ctypes.POINTER(Statvfs)]

    ##########################
    # COLETA DE DADOS DA CPU #
    ##########################

    """
    Lê os dados da CPU a partir do arquivo /proc/stat.

    Returns:
        list: Inteiros.
    """
    def cpu_file_reader(self):
        with open('/proc/stat', 'r') as file:
            cpu_time = (file.readline()).split()[1:]
        return list(map(int, cpu_time))

    """
    Lê informações estáticas da CPU a partir do arquivo /proc/cpuinfo.

    Returns:
        cpu_model_name: String com dados do modelo da CPU.
    """
    def cpu_data_collector(self):
        with open('/proc/cpuinfo', 'r') as file:
            cpu_model_name = file.readlines()[4].split()[3:]

        return cpu_model_name

    """
    Trata informações dinâmicas da CPU, como porcentagem de uso e tempo ocioso.

    Returns:
        cpu_percent_processed: (type, percent), String e float respectivamente.
    """
    def cpu_percent_collector(self):
        cpu_percent_processed = {}

        # Busca informações da CPU com delay de um segundo
        time_init = self.cpu_file_reader()
        time.sleep(0.5)
        time_end = self.cpu_file_reader()

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
        cpu_percent_processed['cpu_usage_percent'] = round(cpu_usage_percent, 1)
        cpu_percent_processed['cpu_idle_percent'] = round(cpu_idle_percent, 1)

        return cpu_percent_processed

    ##############################
    # COLETA DE DADOS DA MEMÓRIA #
    ##############################

    """
    Lê todos os dados sobre a memória a partir do arquivo /proc/meminfo.

    Returns:
        memory_info: (key, data), String e inteiro respectivamente.
    """
    def memory_file_reader(self):
        memory_info = {}

        with open('/proc/meminfo', 'r') as file:
            for line in file:
                key, value = line.split(':')
                memory_info[key.strip()] = int(value.strip().split()[0])

        return memory_info

    """
    Filtra informações estáticas da memória.

    Returns:
        memory_data_processed: (type, data), String e inteiro respectivamente.
    """
    def memory_data_collector(self):
        memory_data_processed = {}
        memory_info = self.memory_file_reader()
        conversion_factor = 1048576

        # Separa informações úteis do dicionário inicial
        total_memory = round(memory_info['MemTotal'] / conversion_factor, 2)
        total_swap = round(memory_info['SwapTotal'] / conversion_factor, 2)
        total_vmem = total_memory + total_swap

        # Adiciona as informações no dicionário final
        memory_data_processed['total_memory'] = total_memory
        memory_data_processed['total_vmem'] = total_vmem
        memory_data_processed['total_swap'] = total_swap

        return memory_data_processed

    """
    Trata informações dinâmicas da memória, como memória usada, memória virtual usada, etc.

    Returns:
        memory_percent_processed: (type, percent), String e float respectivamente.
    """
    def memory_percent_collector(self):
        conversion_factor = 1048576
        memory_percent_processed = {}
        memory_info = self.memory_file_reader()

        # Memória física
        total_memory = memory_info['MemTotal']
        free_memory = (memory_info['MemFree'] + memory_info['Buffers'] + memory_info['Cached'])
        used_memory = total_memory - free_memory

        # Memória swap
        total_swap = memory_info['SwapTotal']
        free_swap = memory_info['SwapFree']
        used_swap = total_swap - free_swap

        # Memória virtual = RAM + Swap
        total_vmem = total_memory + total_swap
        used_vmem = used_memory + used_swap
        free_vmem = total_vmem - used_vmem

        # Porcentagens
        memory_usage_percent = (used_memory / total_memory) * 100
        memory_free_percent = 100 - memory_usage_percent

        vmem_usage_percent = (used_vmem / total_vmem) * 100 if total_vmem > 0 else 0
        vmem_free_percent = 100 - vmem_usage_percent

        # Dicionário com as porcentagens de uso das memórias
        memory_percent_processed['memory_usage_percent'] = round(memory_usage_percent, 1)
        memory_percent_processed['memory_usage'] = round(used_memory / conversion_factor, 2)
        memory_percent_processed['memory_free_percent'] = round(memory_free_percent, 1)
        memory_percent_processed['memory_free'] = round(free_memory / conversion_factor, 2)
        memory_percent_processed['vmem_usage_percent'] = round(vmem_usage_percent, 1)
        memory_percent_processed['vmem_usage'] = round(used_vmem / conversion_factor, 2)
        memory_percent_processed['vmem_free_percent'] = round(vmem_free_percent, 1)
        memory_percent_processed['vmem_free'] = round(free_vmem / conversion_factor, 2)

        return memory_percent_processed

    #################################
    # COLETA DE DADOS DOS PROCESSOS #
    #################################


    """
    Responsável por lidar com links do sistema linux, usando a biblioteca ctypes e chamadas de sistema.

    Returns:
        String contendo informações do link
    """
    def readlink(self, path, buffer_size=4096):
        buf = ctypes.create_string_buffer(buffer_size)
        path_bytes = str(path).encode('utf-8')
        result = self.libc.readlink(path_bytes, buf, buffer_size)
        if result == -1:
            errno = ctypes.get_errno()
            raise OSError(errno, f"Erro ao ler link: {path}")
        return buf.value.decode()

    """
    Responsável por coletar os recursos de cada processo.

    Returns:
        resources: (type, list), String e lista respectivamente.
    """
    def get_process_resources(self, pid):
        # Cria o dicionário de recursos do processo
        fd_dir = Path(f"/proc/{pid}/fd")
        resources = {
            "arquivos": [],
            "sockets": [],
            "pipes": [],
            "eventfd": [],
            "inotify": [],
            "outros": []
        }

        try:
            # Looping para ler os links e informações
            for fd_path in fd_dir.iterdir():
                try:
                    target = self.readlink(fd_path)
                    if "socket:" in target:
                        resources["sockets"].append(target)
                    elif "pipe:" in target:
                        resources["pipes"].append(target)
                    elif "eventfd" in target:
                        resources["eventfd"].append(target)
                    elif "inotify" in target:
                        resources["inotify"].append(target)
                    elif "anon_inode" in target:
                        resources["outros"].append(target)
                    else:
                        resources["arquivos"].append(target)
                except Exception as e:
                    resources["outros"].append(f"{fd_path.name}: erro ao ler ({e})")
        except Exception as e:
            print(f"Erro ao acessar /proc/{pid}/fd: {e}")
        
        return resources

    """
    Busca o usuário correspondente ao uid recebido por parâmetro no arquivo /etc/passwd.

    Returns:
        split[0]: String com o nome do usuário, se reconhecido.
    """
    def get_user_from_uid(self, uid):
        with open('/etc/passwd', 'r') as file:
            passwd = file.readlines()

        # Verifica linha por linha em busca de um uid igual ao do parâmetro
        for line in passwd:
            split = line.split(':')
            if split[2] == uid:
                return split[0]

        return 'unknown'

    """
    Coleta dados dos processos e Threads dos processos ativos na pasta /proc/.

    Returns:
        processes: (process_data, ..., process_data) Lista de dicionários, cada dicionário representando um processo com suas respectivas
        informações. Dentro de cada dicionário, há uma lista (id, nome) com o id e nome de cada thread do respectivo processo.
    """
    def process_data_collector(self):
        processes = []
        path = Path('/proc')

        # Itera nos diretórios e verifica se são processos
        for process_id in path.iterdir():
            if process_id.is_dir() and process_id.name.isdigit():
                process_data = {}

                # Salva id do processo
                process_data['process_id'] = process_id.name

                # Salva os recursos usados pelo processo
                process_data['resources'] = self.get_process_resources(process_id.name)

                # Bloco try para verificar se os processos ainda existem durante o acesso aos mesmos
                try:
                    status_file = process_id / 'status'

                    # Leitura do arquivo status do processo
                    with open (status_file, 'r') as file:
                        status_lines = file.readlines()

                    # Identificação do usuário dono do processo
                    for line in status_lines:
                        if line.startswith('Uid:'):
                            uid = line.split()[1]
                            process_data['user'] = self.get_user_from_uid(uid)
                            break

                        if line.startswith('Name:'):
                            process_data['name'] = line.split()[1]

                    process_data['vm_size'] = "-"
                    process_data['m_size'] = "-"
                    process_data['heap'] = "-"
                    process_data['stack'] = "-"
                    process_data['data'] = "-"

                    # Filtro de outros dados importantes
                    for line in status_lines:

                        key = line.split(':')[0]
                        value = line.split(':')[1].strip()

                        match key:
                            # Tamanho da memória virtual
                            case 'VmSize':
                                process_data['vm_size'] = value 
                            # Tamanho da memória física
                            case 'VmRSS':
                                process_data['m_size'] = value
                            # Tamanho da heap
                            case 'VmData':
                                process_data['heap'] = value
                            # Tamanho da stack
                            case 'VmStk':
                                process_data['stack'] = value
                            #Tamanho do data
                            case 'VmExe':
                                process_data['data'] = value

                    # Coleta de informação sobre as threads do processo
                    task_dir = process_id / 'task'

                    if task_dir.exists():
                        thread_data = []
                        for thread_dir in task_dir.iterdir():
                            thread_status = thread_dir / 'status'

                            # Salva o id e o nome da thread em uma lista
                            if thread_status.exists():
                                with open(thread_status, 'r') as file:
                                    name = file.readline().strip()


                                thread_data.append(thread_dir.name +' '+ name.split()[1])

                        # Adiciona a lista de threads no dicionário do processo
                        process_data['thread_data'] = thread_data
                        process_data['n_threads'] = len(thread_data)

                    # Adiciona o processo em uma lista
                    processes.append(process_data)


                except Exception:
                    continue

        # Itera pelos processos para saber o número total de threads
        n_threads = 0
        for process in processes:
            n_threads += len(process['thread_data'])

        return processes, n_threads


if __name__ == "__main__":
    data_collector = DataCollector()

    data_collector.process_data_collector()
