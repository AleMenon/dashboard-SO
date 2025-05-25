"""
controller.py

Esse módulo é responsável por fazer a transferência de dados entre o data_collector e a interface.
"""

import threading
import time

class Controller:
    #Construtor
    def __init__(self, data_collector, interface, root):
        self.data_collector = data_collector
        self.interface = interface
        self.root = root  # Referência ao Tkinter root para usar after()
        self.running = False
        self.thread = None

    """
    Inicializa os dados estáticos na interface.

    Returns:
        NULL.
    """
    def setup(self):
        memory_static_data = self.data_collector.memory_data_collector()
        conversion_factor = 1048576
        
        # Conversão de dados da memória de kb para gb
        memory_static_data['total_memory'] = memory_static_data['total_memory'] / conversion_factor
        memory_static_data['total_vmem'] = memory_static_data['total_vmem'] / conversion_factor

        #######################################################################
        # Atualiza dados estáticos logo no início (ex.: total de memória)     #
        #######################################################################
        # Aqui tem que ser chamado um método para coletar os dados            #
        # estáticos da memória e da cpu, e envio para a interface. Exemplo de #
        # implementação abaixo.                                               #
        # P.S.: Não precisa ser necessariamente esse nome para o método na    #
        # interface.                                                          #
        #######################################################################
        self.interface.update_static_data(memory_static_data, self.data_collector.cpu_data_collector())

    """
    Inicia a thread responsável por rodar o backend e a coleta de dados.

    Returns:
        NULL.
    """
    def start(self):
        self.setup()
        self.running = True
        self.thread = threading.Thread(target=self.update_loop, daemon=True)
        self.thread.start()

    """
    Resposável por encerrar a thread do backend.

    Returns:
        NULL.
    """
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    """
    Método responsável por atualizar os dados na interface a cada 5 segundos.

    Returns:
        NULL.
    """
    def update_loop(self):
        while self.running:
            # Coleta os dados
            conversion_factor = 1048576
            cpu_percent = self.data_collector.cpu_percent_collector()
            memory_percent = self.data_collector.memory_percent_collector()
            processes_data = self.data_collector.process_data_collector()

            # Conversão dos dados da memória de kb para gb
            memory_percent['memory_usage'] = memory_percent['memory_used'] / conversion_factor
            memory_percent['memory_free'] = memory_percent['memory_free'] / conversion_factor
            memory_percent['vmem_usage'] = memory_percent['vmem_usage'] / conversion_factor
            memory_percent['vmem_free'] = memory_percent['vmem_free'] / conversion_factor

            # Número de processos
            n_processes = len(processes_data)

            n_threads = 0

            # Número de threads
            for process in processes_data:
                n_threads += len(process['thread_data'])

            ##################################################################
            # Envia os dados pra interface usando Tkinter (thread-safe)      #
            ##################################################################
            # Esse método after é fornecido pela biblioteca do tkinter:      #
            #                                                                #
            # after(delay_ms, callback, *args)                               #
            #   delay_ms: Tempo em milissegundos antes de executar o método; #
            #   callback: Função que é pra ser executada;                    #
            #   *args: Argumento que é passado para a função                 #
            ##################################################################

            self.root.after(0, self.interface.update_data, {    
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'process_data': processes_data,
                'n_processes' : n_processes,
                'n_threads' : n_threads,
            })

            # Espera 5 segundos pra próxima atualização
            time.sleep(5)  
