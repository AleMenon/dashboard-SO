"""
main.py

Esse módulo apresenta a implementação da main, que inicializa e executa todo o código para funcionamento do programa.
"""

import tkinter as tk
from data_collector import DataCollector 
from interface import Interface
from controller import Controller

# Executa somente se esse programa é chamado diretamente na compilação
if __name__ == "__main__":

    # Tkinter
    root = tk.Tk()

    # Inicialização das classes
    data_collector = DataCollector()

    processes_data = data_collector.process_data_collector()
    n_threads = 0

    # Número de threads
    for process in processes_data:
        n_threads += len(process['thread_data'])

    interface = Interface(root, n_threads)
    controller = Controller(data_collector, interface, root)

    controller.start()

    try:
        root.mainloop()
    finally:
        controller.stop()
