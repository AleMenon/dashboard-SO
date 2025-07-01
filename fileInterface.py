import tkinter as tk
from tkinter import ttk, messagebox

class FileInterface(tk.Frame):
    def __init__(self, parent, controller, fs_collector, file_tree):
        super().__init__(parent, bg="#dcdcdc")

        self.controller = controller
        self.fs_collector = fs_collector
        self.file_tree = file_tree

        self.current_path = tk.StringVar(value="/")

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)

        self.create_header()
        self.create_mount_table()
        self.create_path_table()
        self.create_nav_buttons()  # Só subir nível

        self.refresh_mount_table()
        self.populate_root_path()

    def create_header(self):
        op_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=10)
        op_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=50, pady=10)
        op_frame.grid_columnconfigure(0, weight=1)

        label = tk.Label(op_frame, text="Gerenciador de Arquivos", font=("Arial", 16), fg="black")
        label.pack(anchor="center")

        back_btn = tk.Button(op_frame, text="Voltar Dashboard",
                             command=lambda: self.controller.show_frame("DashboardFrame"))
        back_btn.pack(side="right")

    def create_mount_table(self):
        self.mount_frame = tk.Frame(self, bg="#dcdcdc")
        self.mount_frame.grid(row=1, column=0, columnspan=3, padx=50, pady=10, sticky="nsew")

        columns = ("Ponto de Montagem", "Total (GB)", "Usado (GB)", "Livre (GB)", "Uso (%)")
        self.mount_tree = ttk.Treeview(self.mount_frame, columns=columns, show="headings", height=5)

        for col in columns:
            self.mount_tree.heading(col, text=col)
            self.mount_tree.column(col, anchor="center", width=120)

        self.mount_tree.pack(fill="x", expand=True)

    def create_path_table(self):
        self.path_frame = tk.Frame(self, bg="#dcdcdc")
        self.path_frame.grid(row=2, column=0, columnspan=3, padx=50, pady=10, sticky="nsew")

        columns = ("Nome", "Tipo", "Tamanho (Bytes)", "Data Modificação", "Permissões")

        self.path_tree = ttk.Treeview(self.path_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.path_tree.heading(col, text=col)
            self.path_tree.column(col, anchor="w", width=150)

        self.path_tree.pack(fill="both", expand=True)

        self.path_tree.bind("<Double-1>", self.on_double_click)

    def create_nav_buttons(self):
        nav_frame = tk.Frame(self, bg="#dcdcdc")
        nav_frame.grid(row=3, column=0, columnspan=3, padx=50, pady=5, sticky="ew")

        up_btn = tk.Button(nav_frame, text="Subir um nível", command=self.go_up)
        up_btn.pack(side="left", padx=5)

    def refresh_mount_table(self):
        mounts = self.fs_collector.get_mounts()

        for row in self.mount_tree.get_children():
            self.mount_tree.delete(row)

        for mount in mounts:
            usage = self.fs_collector.get_fs_usage(mount)
            if usage:
                total, used, free, percent = usage
                self.mount_tree.insert("", "end", values=(
                    mount,
                    f"{total / (1024 ** 3):.2f}",
                    f"{used / (1024 ** 3):.2f}",
                    f"{free / (1024 ** 3):.2f}",
                    f"{percent:.1f}%"
                ))

    def populate_root_path(self):
        for row in self.path_tree.get_children():
            self.path_tree.delete(row)
        self.path_tree.insert("", "end", values=("/", "Diretório"))

    def on_double_click(self, event):
        selected_item = self.path_tree.focus()
        if not selected_item:
            return

        values = self.path_tree.item(selected_item)["values"]
        name = values[0]
        tipo = values[1]

        if name == "/":
            new_path = "/"
        else:
            base = self.current_path.get().rstrip("/")
            new_path = f"{base}/{name}" if base != "/" else f"/{name}"

        if new_path.startswith("/proc"):
            messagebox.showwarning(" Bloqueado", f"Navegação para {new_path} não é permitida!")
            return

        self.current_path.set(new_path)
        self.refresh_directory()

    def refresh_directory(self):
        path = self.current_path.get().strip()

        content = self.file_tree.list_content(path)

        for row in self.path_tree.get_children():
            self.path_tree.delete(row)

        if not content:
            messagebox.showinfo("Aviso", f"Nenhum conteúdo em {path}")
            return

        for item in content:
            self.path_tree.insert("", "end", values=(
                item["name"],
                item["type"],
                item["size"],
                item["mod_time"],
                item["permissions"]
            ))

    def go_up(self):
        path = self.current_path.get().rstrip("/")
        if path == "" or path == "/":
            return

        parts = [p for p in path.split("/") if p]
        if parts:
            parts.pop()

        new_path = "/" + "/".join(parts) if parts else "/"

        self.current_path.set(new_path)
        self.refresh_directory()
