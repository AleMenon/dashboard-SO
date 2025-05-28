import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Projeto A")
        self.root.geometry("1800x900")
        self.root.configure(bg="#dcdcdc")
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
        self.tablep_tree = None
        self.process_tree = None


        # Configure the grid layout for the main window
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)

        self.create_op_frame()

    def create_op_frame(self):
        op_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        op_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        op_frame.grid_columnconfigure(0, weight=1)

        label = tk.Label(op_frame, text="Operation System", font=("Arial", 16), fg="black")
        label.grid(row=0, column=0, sticky="nsew")

    def pie_chart_memory(self, data_memory):
        data_percent = data_memory["memory_free_percent"]

        if self.memory_chart_frame is None:
            self.memory_chart_frame = tk.Frame(self.root)
            self.memory_chart_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

            self.memory_fig, self.memory_ax = plt.subplots(figsize=(3.5, 3.5))
            self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=self.memory_chart_frame)
            self.memory_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.memory_ax.clear()
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100 - data_percent]
        colors = ['green', 'red']
        self.memory_ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        self.memory_ax.set_title("Memory Status")
        self.memory_canvas.draw()

    def pie_chart_virtual_memory(self, data_virtual_memory):
        data_percent = data_virtual_memory["vmem_free_percent"]

        if self.virtual_memory_chart_frame is None:
            self.virtual_memory_chart_frame = tk.Frame(self.root)
            self.virtual_memory_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            self.virtual_memory_fig, self.virtual_memory_ax = plt.subplots(figsize=(3.5, 3.5))
            self.virtual_memory_canvas = FigureCanvasTkAgg(self.virtual_memory_fig, master=self.virtual_memory_chart_frame)
            self.virtual_memory_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.virtual_memory_ax.clear()
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100 - data_percent]
        colors = ['green', 'red']
        self.virtual_memory_ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        self.virtual_memory_ax.set_title("Virtual Memory Status")
        self.virtual_memory_canvas.draw()

    def pie_chart_cpu(self, data_cpu):
        data_percent = data_cpu["cpu_idle_percent"]

        if self.cpu_chart_frame is None:
            self.cpu_chart_frame = tk.Frame(self.root)
            self.cpu_chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.cpu_fig, self.cpu_ax = plt.subplots(figsize=(3.5, 3.5))
            self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_chart_frame)
            self.cpu_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.cpu_ax.clear()
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100.0 - data_percent]
        colors = ['green', 'red']
        self.cpu_ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        self.cpu_ax.set_title("CPU Status")
        self.cpu_canvas.draw()

    def dinamic_data_table(self, memory_data):
        if self.memory_frame is None:
            self.memory_frame = tk.Frame(self.root, bg="#dcdcdc")
            self.memory_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.memory_frame, text="Memory Information", font=("Arial", 14, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, pady=(0, 5), sticky="w")

            columns = ("Info", "Gb", "Percent")
            self.memory_tree = ttk.Treeview(self.memory_frame, columns=columns, show='headings', height=6)
            self.memory_tree.grid(row=1, column=0, sticky="nsew")

            self.memory_tree.heading("Info", text=" ")
            self.memory_tree.heading("Gb", text="GB")
            self.memory_tree.heading("Percent", text="PERCENT")

            self.memory_tree.column("Info", width=300, anchor="w")
            self.memory_tree.column("Gb", width=200, anchor="center")
            self.memory_tree.column("Percent", width=200, anchor="center")

        # Atualiza os dados da tabela
        # Primeiro limpa os itens antigos
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)

        # Depois insere os novos dados
        rows = [
            ("Free Memory", memory_data["memory_free"], memory_data["memory_free_percent"]),
            ("Used Memory", memory_data["memory_usage"], memory_data["memory_usage_percent"]),
            ("Free Virtual Memory", memory_data["vmem_free"], memory_data["vmem_free_percent"]),
        ]

        for row in rows:
            self.memory_tree.insert("", "end", values=row)

    def static_data_table(self, static_data):

        static_data_frame = tk.Frame(self.root, bg="#dcdcdc")
        static_data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        label = tk.Label(static_data_frame, text="Static Data", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, pady=(0, 5), sticky="w")

        columns = ("Info", "Gb", "Percent")
        tree = ttk.Treeview(static_data_frame, columns=columns, show='headings', height=2)
        tree.grid(row=1, column=0, sticky="nsew")

        tree.heading("Info", text=" ")
        tree.heading("Gb", text="GB")
        tree.heading("Percent", text="PERCENT")

        tree.column("Info", width=300, anchor="w")
        tree.column("Gb", width=200, anchor="center")
        tree.column("Percent", width=200, anchor="center")

        rows = [
            ("Total Memory", static_data["total_memory"], "100.0"),
            ("Total Virtual Memory", static_data["total_vmem"], "100.0"),
        ]

        for row in rows:
            tree.insert("", "end", values=row)

    def show_process_and_threads_table(self, process_threads_data, n_threads):
        if self.tablept_frame is None:
            self.tablept_frame = tk.Frame(self.root, bg="#dcdcdc")
            self.tablept_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.tablept_frame, text="Process X Threads", font=("Arial", 14, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, pady=(0, 5), sticky="w")

            columns = ("Info", "Numbers")
            self.tablept_tree = ttk.Treeview(self.tablept_frame, columns=columns, show='headings', height=2)
            self.tablept_tree.grid(row=1, column=0, sticky="nsew")

            self.tablept_tree.heading("Info", text=" ")
            self.tablept_tree.heading("Numbers", text="NUMBERS")

            self.tablept_tree.column("Info", width=300, anchor="w")
            self.tablept_tree.column("Numbers", width=200, anchor="center")

        # Limpa os dados antigos
        for item in self.tablept_tree.get_children():
            self.tablept_tree.delete(item)

        # Insere os novos dados
        rows = [
            ("Processes", len(process_threads_data)),
            ("Threads", n_threads),
        ]

        for row in rows:
            self.tablept_tree.insert("", "end", values=row)

    def show_process_table(self, processes_data):
        if self.tablep_frame is None:
            self.tablep_frame = tk.Frame(self.root, bg="#dcdcdc")
            self.tablep_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.tablep_frame, text="Processes Information", font=("Arial", 12, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, pady=(10, 5), sticky="w")

            inner_frame = tk.Frame(self.tablep_frame)
            inner_frame.grid(row=1, column=0, sticky="nsew")

            scrollbar = tk.Scrollbar(inner_frame)
            scrollbar.pack(side="right", fill="y")

            columns = (
                "Process ID", "Name", "User", "Memory Used",
                "Virtual Memory Used", "Stack", "Heap", "Data", "Number of Threads"
            )

            column_widths = {
                "Process ID": 100,
                "Name": 300,
                "User": 120,
                "Memory Used": 160,
                "Virtual Memory Used": 270,
                "Stack": 100,
                "Heap": 100,
                "Data": 100,
                "Number of Threads": 270
            }

            self.process_tree = ttk.Treeview(inner_frame, columns=columns, show='headings',
                                             yscrollcommand=scrollbar.set)

            for col in columns:
                self.process_tree.heading(col, text=col.upper())
                self.process_tree.column(col, width=column_widths.get(col, 100), anchor="w")

            self.process_tree.pack(fill="both", expand=True)
            scrollbar.config(command=self.process_tree.yview)

        # Este bloco atualiza os dados da tabela sem recriá-la
        if self.process_tree is not None:
            # Limpa linhas antigas
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)

            # Adiciona os novos dados
            for process in processes_data:
                self.process_tree.insert("", "end", values=(
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

    def update_data_cpu(self, data):
        self.pie_chart_cpu(data)

    def update_data_memory(self, data):
        self.pie_chart_memory(data)
        self.pie_chart_virtual_memory(data)
        self.dinamic_data_table(data)

    def update_data_process(self, process, n_threads):
        self.show_process_table(process)
        self.show_process_and_threads_table(process, n_threads)
