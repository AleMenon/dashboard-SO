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

        process_data = self.data_collector.process_data_collector()

        # self.interface.update_static_data(self.data_collector.cpu_data_collector()) # Alterar nome do método depois
        self.interface.show_process_table(process_data[0])
        self.interface.pie_chart_memory(self.data_collector.memory_percent_collector())
        self.interface.pie_chart_virtual_memory(self.data_collector.memory_percent_collector())
        self.interface.pie_chart_cpu(self.data_collector.cpu_percent_collector())
        self.interface.show_memory_table(self.data_collector.memory_percent_collector())
        self.interface.show_process_and_threads_table(process_data[0], process_data[1])

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
            cpu_percent = self.data_collector.cpu_percent_collector()
            memory_percent = self.data_collector.memory_percent_collector()
            processes_data = self.data_collector.process_data_collector()

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
                'process_data': processes_data[0],
                'n_threads' : processes_data[1],
            })

            # Espera 5 segundos pra próxima atualização
            time.sleep(5)  
