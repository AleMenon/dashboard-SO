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
from file_interface import FileInterface


class Controller:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Operacional")

        # Força cálculo da tela
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)

        # Evita valores zero ou negativos
        width = max(width, 400)
        height = max(height, 300)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.data_collector = DataCollector()
        self.fs_collector = FileSystemCollector()

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}


        dashboard = Interface(self.container, self, self.data_collector)
        dashboard.grid(row=0, column=0, sticky="nsew")
        self.frames["DashboardFrame"] = dashboard


        file_frame = FileInterface(self.container, self, self.fs_collector)
        file_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["FileFrame"] = file_frame


        self.running = False
        self.cpu_thread = None
        self.memory_thread = None
        self.process_thread = None

    """
    Exibe um frame específico com base no nome fornecido.
    Permite alternar entre as telas (Dashboard ou FileInterface).
    """

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    """
    Realiza a configuração inicial:
    - Coleta os dados iniciais
    - Preenche tabelas e gráficos com valores estáticos e primeiros valores dinâmicos
    """

    def setup(self):
        dashboard = self.frames["DashboardFrame"]
        process_data = self.data_collector.process_data_collector()

        dashboard.static_data_table(self.data_collector.memory_data_collector())
        dashboard.show_process_table(process_data[0])
        dashboard.pie_chart_memory(self.data_collector.memory_percent_collector())
        dashboard.pie_chart_virtual_memory(self.data_collector.memory_percent_collector())
        dashboard.pie_chart_cpu(self.data_collector.cpu_percent_collector())
        dashboard.dinamic_data_table(self.data_collector.memory_percent_collector())
        dashboard.show_process_and_threads_table(process_data[0], process_data[1])

    """
    Inicia a aplicação:
    - Executa a configuração inicial
    - Cria e inicia as threads de atualização para CPU, memória e processos
    - Exibe o dashboard inicial
    - Executa o loop principal do Tkinter
    """

    def start(self):
        self.setup()
        self.running = True

        self.cpu_thread = threading.Thread(target=self.cpu_update_loop, daemon=True)
        self.cpu_thread.start()

        self.memory_thread = threading.Thread(target=self.memory_update_loop, daemon=True)
        self.memory_thread.start()

        self.process_thread = threading.Thread(target=self.process_update_loop, daemon=True)
        self.process_thread.start()

        self.show_frame("DashboardFrame")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.close()

    """
    Fecha a aplicação de forma segura:
    - Interrompe as threads de coleta
    - Fecha a janela principal do Tkinter
    """

    def close(self):
        self.running = False
        if self.root.winfo_exists():
            self.root.quit()
            self.root.destroy()

    """
    Loop de atualização contínua da CPU.
    É executado em uma thread separada.
    Coleta os dados de uso da CPU e solicita atualização na interface.
    """

    def cpu_update_loop(self):

        while self.running:
            cpu_percent = self.data_collector.cpu_percent_collector()
            if not self.running:
                break
            self.root.after(0, self.frames["DashboardFrame"].update_data_cpu, cpu_percent)
            time.sleep(1)

    """
    Loop de atualização contínua da memória (RAM e virtual).
    Executa em uma thread separada.
    Coleta os dados de uso de memória e solicita atualização na interface.
    """

    def memory_update_loop(self):

        while self.running:
            memory_percent = self.data_collector.memory_percent_collector()
            if not self.running:
                break
            self.root.after(0, self.frames["DashboardFrame"].update_data_memory, memory_percent)
            time.sleep(1)

    """
    Loop de atualização contínua da lista de processos.
    Executa em uma thread separada.
    Coleta os dados dos processos em execução e solicita atualização na interface.
    """

    def process_update_loop(self):
        while self.running:
            processes_data = self.data_collector.process_data_collector()
            if not self.running:
                break
            self.root.after(0, self.frames["DashboardFrame"].update_data_process, processes_data[0], processes_data[1])
            time.sleep(1)
