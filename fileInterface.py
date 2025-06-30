import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class FileInterface(tk.Frame):
    def __init__(self, parent, controller, data_collector):
        super().__init__(parent, bg="#dcdcdc")

        self.controller = controller
        self.data_collector = data_collector

        # Configuração de grid se precisar
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

        # Título da tela
        label = tk.Label(self, text="Tela de Arquivos", font=("Arial", 18, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, padx=20, pady=20)

        # Botão para voltar para o Dashboard
        back_btn = tk.Button(
            self,
            text="Voltar para o Dashboard",
            command=lambda: self.controller.show_frame("DashboardFrame")
        )
        back_btn.grid(row=1, column=0, pady=10)
