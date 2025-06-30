"""
controller.py

Esse módulo é responsável por fazer a transferência de dados entre o data_collector e a interface.
"""

import tkinter as tk
from data_collector import DataCollector 
from interface import Interface
import threading
import time

class Controller:
    #Construtor
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.data_collector = DataCollector()
        self.interface = Interface(self.root, self.data_collector)
        self.running = False

        # Threads
        self.cpu_thread = None
        self.memory_thread = None
        self.process_thread = None

    """
    Inicializa os dados estáticos na interface.

    Returns:
        NULL.
    """
    def setup(self):

        process_data = self.data_collector.process_data_collector()

        # Construção da interface e inserção dos dados iniciais
        self.interface.static_data_table(self.data_collector.memory_data_collector())
        self.interface.show_process_table(process_data[0])
        self.interface.pie_chart_memory(self.data_collector.memory_percent_collector())
        self.interface.pie_chart_virtual_memory(self.data_collector.memory_percent_collector())
        self.interface.pie_chart_cpu(self.data_collector.cpu_percent_collector())
        self.interface.dinamic_data_table(self.data_collector.memory_percent_collector())
        self.interface.show_process_and_threads_table(process_data[0], process_data[1])

    """
    Inicia a thread responsável por rodar o backend e a coleta de dados.

    Returns:
        NULL.
    """
    def start(self):
        self.setup()
        self.running = True

        # Criação e início da thread de CPU
        self.cpu_thread = threading.Thread(target=self.cpu_update_loop, daemon=True)
        self.cpu_thread.start()

        # Criação e início da thread de memória
        self.memory_thread = threading.Thread(target=self.memory_update_loop, daemon=True)
        self.memory_thread.start()

        # Criação e início da thread de processos
        self.process_thread = threading.Thread(target=self.process_update_loop, daemon=True)
        self.process_thread.start()

        self.root.mainloop()

    """
    Resposável por encerrar a thread do backend e destruir a janela.

    Returns:
        NULL.
    """
    def close(self):
        self.running = False
        self.root.destroy()

    """
    Método executado pela thread, responsável pela coleta de dados da CPU.

    Returns:
        NULL.
    """
    def cpu_update_loop(self):
        while self.running:
            cpu_percent = self.data_collector.cpu_percent_collector()

            self.root.after(0, self.interface.update_data_cpu, cpu_percent)

            time.sleep(1)

    """
    Método executado pela thread, responsável pela coleta de dados da memória.

    Returns:
        NULL.
    """
    def memory_update_loop(self):
        while self.running:
            memory_percent = self.data_collector.memory_percent_collector()

            self.root.after(0, self.interface.update_data_memory, memory_percent)

            time.sleep(1)

    """
    Método executado pela thread, responsável pela coleta de dados dos processos.

    Returns:
        NULL.
    """
    def process_update_loop(self):
        while self.running:
            processes_data = self.data_collector.process_data_collector()

            self.root.after(0, self.interface.update_data_process, processes_data[0], processes_data[1])

            time.sleep(1)