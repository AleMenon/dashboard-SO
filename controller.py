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
from file_tree import FileTree


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Operacional")
        self.root.geometry("1920x1080")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.data_collector = DataCollector()
        self.fs_collector = FileSystemCollector()
        self.file_tree = FileTree()

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Dashboard principal
        dashboard = Interface(self.container, self, self.data_collector)
        dashboard.grid(row=0, column=0, sticky="nsew")
        self.frames["DashboardFrame"] = dashboard

        # Segunda tela
        file_frame = FileInterface(self.container, self, self.fs_collector, self.file_tree)
        file_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["FileFrame"] = file_frame

        # Controle das threads
        self.running = False
        self.cpu_thread = None
        self.memory_thread = None
        self.process_thread = None

    def show_frame(self, frame_name):
        """Exibe o frame desejado e gerencia o monitoramento"""
        frame = self.frames[frame_name]
        frame.tkraise()

        if frame_name == "DashboardFrame":
            self.running = True
            self.ensure_threads_running()

        elif frame_name == "FileFrame":
            self.running = False

    def setup(self):
        """Inicializa os dados estáticos na interface."""
        dashboard = self.frames["DashboardFrame"]
        process_data = self.data_collector.process_data_collector()

        dashboard.static_data_table(self.data_collector.memory_data_collector())
        dashboard.show_process_table(process_data[0])
        dashboard.pie_chart_memory(self.data_collector.memory_percent_collector())
        dashboard.pie_chart_virtual_memory(self.data_collector.memory_percent_collector())
        dashboard.pie_chart_cpu(self.data_collector.cpu_percent_collector())
        dashboard.dinamic_data_table(self.data_collector.memory_percent_collector())
        dashboard.show_process_and_threads_table(process_data[0], process_data[1])

    def start(self):
        """Inicia o sistema"""
        self.setup()
        self.running = True
        self.ensure_threads_running()
        self.show_frame("DashboardFrame")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.close()

    def ensure_threads_running(self):
        """Garante que as threads estejam ativas"""
        if self.cpu_thread is None or not self.cpu_thread.is_alive():
            self.cpu_thread = threading.Thread(target=self.cpu_update_loop, daemon=True)
            self.cpu_thread.start()

        if self.memory_thread is None or not self.memory_thread.is_alive():
            self.memory_thread = threading.Thread(target=self.memory_update_loop, daemon=True)
            self.memory_thread.start()

        if self.process_thread is None or not self.process_thread.is_alive():
            self.process_thread = threading.Thread(target=self.process_update_loop, daemon=True)
            self.process_thread.start()

    def close(self):
        """Finaliza tudo com segurança"""
        self.running = False
        if self.root.winfo_exists():
            self.root.quit()
            self.root.destroy()

    def cpu_update_loop(self):
        """Loop CPU"""
        while True:
            if not self.running:
                break
            cpu_percent = self.data_collector.cpu_percent_collector()
            self.root.after(0, self.frames["DashboardFrame"].update_data_cpu, cpu_percent)
            time.sleep(1)

    def memory_update_loop(self):
        """Loop Memória"""
        while True:
            if not self.running:
                break
            memory_percent = self.data_collector.memory_percent_collector()
            self.root.after(0, self.frames["DashboardFrame"].update_data_memory, memory_percent)
            time.sleep(1)

    def process_update_loop(self):
        """Loop Processos"""
        while True:
            if not self.running:
                break
            processes_data = self.data_collector.process_data_collector()
            self.root.after(0, self.frames["DashboardFrame"].update_data_process,
                            processes_data[0], processes_data[1])
            time.sleep(1)
