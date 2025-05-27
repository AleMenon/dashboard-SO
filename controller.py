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
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.data_collector = DataCollector()
        self.interface = Interface(self.root)
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

        # Start CPU thread
        self.cpu_thread = threading.Thread(target=self.cpu_update_loop, daemon=True)
        self.cpu_thread.start()

        # Start Memory thread
        self.memory_thread = threading.Thread(target=self.memory_update_loop, daemon=True)
        self.memory_thread.start()

        # Start Process thread
        self.process_thread = threading.Thread(target=self.process_update_loop, daemon=True)
        self.process_thread.start()

        self.root.mainloop()

    """
    Resposável por encerrar a thread do backend.

    Returns:
        NULL.
    """
    def on_close(self):
        self.stop()
        self.root.destroy()

    def stop(self):
        self.running = False
        """
        for thread in [self.cpu_thread, self.memory_thread, self.process_thread]:
            if thread and thread.is_alive():
                thread.join(timeout=6)
        """


    def cpu_update_loop(self):
        while self.running:
            cpu_percent = self.data_collector.cpu_percent_collector()

            self.root.after(0, self.interface.update_data_cpu, cpu_percent)

            time.sleep(5)

    def memory_update_loop(self):
        while self.running:
            memory_percent = self.data_collector.memory_percent_collector()

            self.root.after(0, self.interface.update_data_memory, memory_percent)

            time.sleep(5)

    def process_update_loop(self):
        while self.running:
            processes_data = self.data_collector.process_data_collector()

            self.root.after(0, self.interface.update_data_process, processes_data[0], processes_data[1])

            time.sleep(5)
