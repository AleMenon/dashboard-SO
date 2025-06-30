"""
controller.py

Esse módulo é responsável por fazer a transferência de dados entre o data_collector e a interface.
"""

import tkinter as tk
import threading
import time

from data_collector import DataCollector
from file_system_collector import FileSystemCollector
from interface import Interface
from fileInterface import FileInterface


class Controller:
    # Construtor
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Operacional")
        self.root.geometry("1920x1080")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.data_collector = DataCollector()
        self.fs_collector = FileSystemCollector()

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Dashboard principal
        dashboard = Interface(self.container, self, self.data_collector)
        dashboard.grid(row=0, column=0, sticky="nsew")
        self.frames["DashboardFrame"] = dashboard

        # Segunda tela
        file_frame = FileInterface(self.container, self, self.fs_collector)
        file_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["FileFrame"] = file_frame

        # Threads
        self.running = False
        self.cpu_thread = None
        self.memory_thread = None
        self.process_thread = None

    def show_frame(self, frame_name):
        """Exibe o frame desejado."""
        frame = self.frames[frame_name]
        frame.tkraise()

    def setup(self):
        """Inicializa os dados estáticos na interface."""
        dashboard = self.frames["DashboardFrame"]
        process_data = self.data_collector.process_data_collector()

        # Construção da interface e inserção dos dados iniciais
        dashboard.static_data_table(self.data_collector.memory_data_collector())
        dashboard.show_process_table(process_data[0])
        dashboard.pie_chart_memory(self.data_collector.memory_percent_collector())
        dashboard.pie_chart_virtual_memory(self.data_collector.memory_percent_collector())
        dashboard.pie_chart_cpu(self.data_collector.cpu_percent_collector())
        dashboard.dinamic_data_table(self.data_collector.memory_percent_collector())
        dashboard.show_process_and_threads_table(process_data[0], process_data[1])

    def start(self):
        """Inicia a thread responsável por rodar o backend e a coleta de dados."""
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

        self.show_frame("DashboardFrame")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.close()

    def close(self):
        """Responsável por encerrar a thread do backend e destruir a janela."""
        #print("Fechando aplicativo com segurança...")
        self.running = False
        if self.root.winfo_exists():
            self.root.quit()
            self.root.destroy()

    def cpu_update_loop(self):
        """Método executado pela thread, responsável pela coleta de dados da CPU."""
        while self.running:
            cpu_percent = self.data_collector.cpu_percent_collector()
            if not self.running:
                break
            self.root.after(0, self.frames["DashboardFrame"].update_data_cpu, cpu_percent)
            time.sleep(1)

    def memory_update_loop(self):
        """Método executado pela thread, responsável pela coleta de dados da memória."""
        while self.running:
            memory_percent = self.data_collector.memory_percent_collector()
            if not self.running:
                break
            self.root.after(0, self.frames["DashboardFrame"].update_data_memory, memory_percent)
            time.sleep(1)

    def process_update_loop(self):
        """Método executado pela thread, responsável pela coleta de dados dos processos."""
        while self.running:
            processes_data = self.data_collector.process_data_collector()
            if not self.running:
                break
            self.root.after(0, self.frames["DashboardFrame"].update_data_process, processes_data[0], processes_data[1])
            time.sleep(1)
