import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Interface(tk.Frame):
    """
    Classe do Dashboard — agora 100% adaptável a qualquer tela.
    """

    def __init__(self, parent, controller, data_collector):
        super().__init__(parent, bg="#dcdcdc")

        self.controller = controller
        self.data_collector = data_collector

        # Configura grid principal
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

        self.cpu_chart_frame = None
        self.memory_chart_frame = None
        self.virtual_memory_chart_frame = None
        self.memory_frame = None
        self.tablept_frame = None
        self.tablep_frame = None

        self.cpu_fig = None
        self.cpu_ax = None
        self.cpu_canvas = None
        self.memory_fig = None
        self.memory_ax = None
        self.memory_canvas = None
        self.virtual_memory_fig = None
        self.virtual_memory_ax = None
        self.virtual_memory_canvas = None

        self.memory_tree = None
        self.static_tree = None
        self.tablept_tree = None
        self.process_tree = None
        self.process_details_map = {}

        self.create_op_frame()

    def create_op_frame(self):
        op_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=10)
        op_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=50, pady=10)

        op_frame.grid_columnconfigure(0, weight=1)
        op_frame.grid_columnconfigure(1, weight=0)

        label = tk.Label(op_frame, text="Sistema Operacional", font=("Arial", 16), fg="black")
        label.grid(row=0, column=0, sticky="w")

        switch_btn = tk.Button(op_frame, text="Arquivos",
                               command=lambda: self.controller.show_frame("FileFrame"))
        switch_btn.grid(row=0, column=1, sticky="e")

    def pie_chart_memory(self, data_memory):
        data_percent = data_memory["memory_free_percent"]

        if self.memory_chart_frame is None:
            self.memory_chart_frame = tk.Frame(self)
            self.memory_chart_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

            self.memory_fig, self.memory_ax = plt.subplots(figsize=(3.5, 3.5))
            self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=self.memory_chart_frame)
            self.memory_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.memory_ax.clear()
        self.memory_ax.pie([data_percent, 100 - data_percent],
                           labels=['Livre', 'Usado'],
                           colors=['green', 'red'],
                           autopct='%1.1f%%')
        self.memory_ax.set_title("Status da Memória")
        self.memory_canvas.draw()

    def pie_chart_virtual_memory(self, data_virtual_memory):
        data_percent = data_virtual_memory["vmem_free_percent"]

        if self.virtual_memory_chart_frame is None:
            self.virtual_memory_chart_frame = tk.Frame(self)
            self.virtual_memory_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            self.virtual_memory_fig, self.virtual_memory_ax = plt.subplots(figsize=(3.5, 3.5))
            self.virtual_memory_canvas = FigureCanvasTkAgg(self.virtual_memory_fig, master=self.virtual_memory_chart_frame)
            self.virtual_memory_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.virtual_memory_ax.clear()
        self.virtual_memory_ax.pie([data_percent, 100 - data_percent],
                                   labels=['Livre', 'Usado'],
                                   colors=['green', 'red'],
                                   autopct='%1.1f%%')
        self.virtual_memory_ax.set_title("Status da Memória Virtual")
        self.virtual_memory_canvas.draw()

    def pie_chart_cpu(self, data_cpu):
        data_percent = data_cpu["cpu_idle_percent"]

        if self.cpu_chart_frame is None:
            self.cpu_chart_frame = tk.Frame(self)
            self.cpu_chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.cpu_fig, self.cpu_ax = plt.subplots(figsize=(3.5, 3.5))
            self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_chart_frame)
            self.cpu_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.cpu_ax.clear()
        self.cpu_ax.pie([data_percent, 100 - data_percent],
                        labels=['Livre', 'Usado'],
                        colors=['green', 'red'],
                        autopct='%1.1f%%')
        self.cpu_ax.set_title("Status da CPU")
        self.cpu_canvas.draw()

    def dinamic_data_table(self, memory_data):
        if self.memory_frame is None:
            self.memory_frame = tk.Frame(self, bg="#dcdcdc")
            self.memory_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            self.memory_frame.grid_columnconfigure(0, weight=1)

            label = tk.Label(self.memory_frame, text="Informações Dinâmicas", font=("Arial", 14, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, sticky="w")

            columns = ("Info", "Gb", "Porcentagem")
            self.memory_tree = ttk.Treeview(self.memory_frame, columns=columns, show='headings', height=3)
            self.memory_tree.grid(row=1, column=0, sticky="nsew")

            for col in columns:
                self.memory_tree.heading(col, text=col)
                self.memory_tree.column(col, anchor="center", stretch=True)

            self.memory_frame.bind("<Configure>", self.resize_memory_columns)

        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)

        rows = [
            ("Memória Livre", memory_data["memory_free"], memory_data["memory_free_percent"]),
            ("Memória Usada", memory_data["memory_usage"], memory_data["memory_usage_percent"]),
            ("Memória Virtual Livre", memory_data["vmem_free"], memory_data["vmem_free_percent"]),
        ]

        for row in rows:
            self.memory_tree.insert("", "end", values=row)

    def resize_memory_columns(self, event):
        total_width = event.width
        self.memory_tree.column("Info", width=max(int(total_width * 0.5), 80))
        self.memory_tree.column("Gb", width=max(int(total_width * 0.25), 50))
        self.memory_tree.column("Porcentagem", width=max(int(total_width * 0.25), 50))

    def static_data_table(self, static_data):
        static_data_frame = tk.Frame(self, bg="#dcdcdc")
        static_data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        static_data_frame.grid_columnconfigure(0, weight=1)

        label = tk.Label(static_data_frame, text="Informações Estáticas", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, sticky="w")

        columns = ("Info", "Gb", "Porcentagem")
        tree = ttk.Treeview(static_data_frame, columns=columns, show='headings', height=3)
        tree.grid(row=1, column=0, sticky="nsew")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", stretch=True)

        self.static_tree = tree
        static_data_frame.bind("<Configure>", self.resize_static_columns)

        rows = [
            ("Memória Total", static_data["total_memory"], "100.0"),
            ("Memória Virtual Total", static_data["total_vmem"], "100.0"),
            ("Swap Total", static_data["total_swap"], "100.0"),
        ]

        for row in rows:
            tree.insert("", "end", values=row)

    def resize_static_columns(self, event):
        total_width = event.width
        self.static_tree.column("Info", width=max(int(total_width * 0.5), 80))
        self.static_tree.column("Gb", width=max(int(total_width * 0.25), 50))
        self.static_tree.column("Porcentagem", width=max(int(total_width * 0.25), 50))

    def show_process_and_threads_table(self, process_threads_data, n_threads):
        if self.tablept_frame is None:
            self.tablept_frame = tk.Frame(self, bg="#dcdcdc")
            self.tablept_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

            self.tablept_frame.grid_columnconfigure(0, weight=1)

            label = tk.Label(self.tablept_frame, text="Processos X Threads", font=("Arial", 14, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, sticky="w")

            columns = ("Info", "Números")
            self.tablept_tree = ttk.Treeview(self.tablept_frame, columns=columns, show='headings', height=2)
            self.tablept_tree.grid(row=1, column=0, sticky="nsew")

            for col in columns:
                self.tablept_tree.heading(col, text=col)
                self.tablept_tree.column(col, anchor="center", stretch=True)

            self.tablept_frame.bind("<Configure>", self.resize_tablept_columns)

        for item in self.tablept_tree.get_children():
            self.tablept_tree.delete(item)

        rows = [
            ("Processos", len(process_threads_data)),
            ("Threads", n_threads),
        ]

        for row in rows:
            self.tablept_tree.insert("", "end", values=row)

    def resize_tablept_columns(self, event):
        total_width = event.width
        self.tablept_tree.column("Info", width=max(int(total_width * 0.7), 80))
        self.tablept_tree.column("Números", width=max(int(total_width * 0.3), 50))

    def show_process_table(self, processes_data):
        if self.tablep_frame is None:
            self.tablep_frame = tk.Frame(self, bg="#dcdcdc")
            self.tablep_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.tablep_frame, text="Informações dos Processos", font=("Arial", 12, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, sticky="w")

            inner_frame = tk.Frame(self.tablep_frame)
            inner_frame.grid(row=1, column=0, sticky="nsew")
            inner_frame.grid_columnconfigure(0, weight=1)
            inner_frame.grid_rowconfigure(0, weight=1)

            scrollbar = tk.Scrollbar(inner_frame)
            scrollbar.pack(side="right", fill="y")

            columns = (
                "ID do Processo", "Nome", "Usuário", "Memória Usada",
                "Memória Virtual Usada", "Stack", "Heap", "Data", "Número de Threads"
            )

            self.process_column_ratios = {
                "ID do Processo": 0.12,
                "Nome": 0.15,
                "Usuário": 0.08,
                "Memória Usada": 0.10,
                "Memória Virtual Usada": 0.18,
                "Stack": 0.07,
                "Heap": 0.07,
                "Data": 0.07,
                "Número de Threads": 0.16
            }

            self.process_tree = ttk.Treeview(inner_frame, columns=columns, show='headings',
                                             yscrollcommand=scrollbar.set)

            for col in columns:
                self.process_tree.heading(col, text=col.upper())
                self.process_tree.column(col, anchor="w", stretch=True)

            self.process_tree.pack(fill="both", expand=True)
            scrollbar.config(command=self.process_tree.yview)

            self.process_tree.bind("<Double-1>", self.on_process_click)

            self.tablep_frame.bind("<Configure>", self.resize_process_columns)

        if self.process_tree and self.process_tree.winfo_exists():
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)

            for process in processes_data:
                item_id = self.process_tree.insert("", "end", values=(
                    process["process_id"],
                    process["name"],
                    process["user"],
                    process["m_size"],
                    process["vm_size"],
                    process["stack"],
                    process["heap"],
                    process["data"],
                    process["n_threads"]
                ))
                self.process_details_map[item_id] = {
                    "pid": process["process_id"],
                    "name": process["name"],
                    "thread_data": process["thread_data"]
                }

    def resize_process_columns(self, event):
        total_width = event.width
        for col, ratio in self.process_column_ratios.items():
            self.process_tree.column(col, width=max(int(total_width * ratio), 50))

    def on_process_click(self, event):
        selected_item = self.process_tree.focus()
        if not selected_item:
            return

        process_info = self.process_details_map.get(selected_item)
        if not process_info:
            return

        pid = process_info["pid"]
        process_info["resources"] = self.data_collector.get_process_resources(pid)
        self.abrir_popup(process_info)

    def abrir_popup(self, process_info):
        popup = tk.Toplevel(self)
        popup.title(f"Detalhes do Processo {process_info['name']} [PID {process_info['pid']}]")
        popup.geometry("600x500")
        popup.configure(bg="#f0f0f0")

        container = tk.Frame(popup)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="Threads:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        for thread in process_info["thread_data"]:
            tk.Label(scrollable_frame, text=f"- {thread}", bg="#f0f0f0").pack(anchor="w", padx=20)

        tk.Label(scrollable_frame, text="\nRecursos:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        for k, v in process_info["resources"].items():
            tk.Label(scrollable_frame, text=f"{k.upper()} ({len(v)})", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(anchor="w")
            for item in v:
                tk.Label(scrollable_frame, text=f" - {item}", bg="#f0f0f0").pack(anchor="w", padx=20)

        tk.Button(popup, text="Fechar", command=popup.destroy).pack(pady=10)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def update_data_cpu(self, data):
        self.pie_chart_cpu(data)

    def update_data_memory(self, data):
        self.pie_chart_memory(data)
        self.pie_chart_virtual_memory(data)
        self.dinamic_data_table(data)

    def update_data_process(self, process, n_threads):
        self.show_process_table(process)
        self.show_process_and_threads_table(process, n_threads)
