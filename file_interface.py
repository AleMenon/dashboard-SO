import tkinter as tk
from tkinter import ttk

"""
Classe responsável por construir e gerenciar a interface gráfica da aba de Sistemas de Arquivos.
Ela exibe informações sobre os sistemas de arquivos montados, como espaço total, usado, livre e porcentagem de uso.
"""

class FileInterface(tk.Frame):
    def __init__(self, parent, controller, fs_collector):
        super().__init__(parent, bg="#dcdcdc")

        self.controller = controller
        self.fs_collector = fs_collector

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)

        self.create_header()
        self.create_table()
        self.refresh_table()

    """
    Cria o cabeçalho da interface, contendo o título "Sistemas de Arquivos"
    e um botão para voltar à tela principal do dashboard.
    """

    def create_header(self):

        op_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=10)
        op_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=50, pady=10)
        op_frame.grid_columnconfigure(0, weight=1)

        label = tk.Label(op_frame, text="Sistemas de Arquivos", font=("Arial", 16), fg="black")
        label.pack(anchor="center")

        back_btn = tk.Button(op_frame, text="Voltar",
                             command=lambda: self.controller.show_frame("DashboardFrame"))
        back_btn.pack(side="right")

    """
    Cria a tabela principal que mostra os pontos de montagem dos sistemas de arquivos,
    juntamente com informações de capacidade total, espaço usado, espaço livre e porcentagem de uso.
    """

    def create_table(self):
        self.table_frame = tk.Frame(self, bg="#dcdcdc")
        self.table_frame.grid(row=1, column=0, columnspan=3, padx=50, pady=20, sticky="nsew")

        columns = ("Ponto de Montagem", "Total (GB)", "Usado (GB)", "Livre (GB)", "Uso (%)")

        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=1)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)  # Adicionei width para melhor visualização

        self.tree.pack(fill="x", expand=True)

    """
    Atualiza os dados exibidos na tabela com informações atualizadas
    dos sistemas de arquivos montados no sistema.
    """

    def refresh_table(self):
        mounts = self.fs_collector.get_mounts()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for mount in mounts:
            usage = self.fs_collector.get_fs_usage(mount)
            if usage:
                total, used, free, percent = usage
                self.tree.insert("", "end", values=(
                    mount,
                    f"{total / (1024 ** 3):.2f}",
                    f"{used / (1024 ** 3):.2f}",
                    f"{free / (1024 ** 3):.2f}",
                    f"{percent:.1f}%"
                ))
