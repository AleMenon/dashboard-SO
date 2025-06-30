import tkinter as tk
from tkinter import ttk

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

    def create_header(self):

        op_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=10)
        op_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=50, pady=10)
        op_frame.grid_columnconfigure(0, weight=1)

        label = tk.Label(op_frame, text="Sistemas de Arquivos", font=("Arial", 16), fg="black")
        label.pack(anchor="center")

        back_btn = tk.Button(op_frame, text="Voltar",
                             command=lambda: self.controller.show_frame("DashboardFrame"))
        back_btn.pack(side="right")

    def create_table(self):
        self.table_frame = tk.Frame(self, bg="#dcdcdc")
        self.table_frame.grid(row=1, column=0, columnspan=3, padx=50, pady=20, sticky="nsew")

        columns = ("Ponto de Montagem", "Total (GB)", "Usado (GB)", "Livre (GB)", "Uso (%)")

        # AQUI: Defina a altura para 1 linha de dados visível
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=1)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)  # Adicionei width para melhor visualização

        # AQUI: Altere o preenchimento para apenas horizontal
        self.tree.pack(fill="x", expand=True)

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
