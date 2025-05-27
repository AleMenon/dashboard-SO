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

        chart_frame = tk.Frame(self.root)
        chart_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100.0 - data_percent]
        colors = ['green', 'red']
        ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title("Memory Status")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def pie_chart_virtual_memory(self, data_virtual_memory):
        data_percent = data_virtual_memory["vmem_free_percent"]

        chart_frame = tk.Frame(self.root)
        chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100.0 - data_percent]
        colors = ['green', 'red']
        ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title("Virtual Memory Status")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def pie_chart_cpu(self, data_cpu):
        data_percent = data_cpu["cpu_idle_percent"]

        chart_frame = tk.Frame(self.root)
        chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100.0 - data_percent]
        colors = ['green', 'red']
        ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title("CPU Status")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def dinamic_data_table(self, memory_data):
        memory_frame = tk.Frame(self.root, bg="#dcdcdc")
        memory_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        label = tk.Label(memory_frame, text="Memory Information", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, pady=(0, 5), sticky="w")

        columns = ("Info", "Gb", "Percent")
        tree = ttk.Treeview(memory_frame, columns=columns, show='headings', height=6)
        tree.grid(row=1, column=0, sticky="nsew")

        tree.heading("Info", text=" ")
        tree.heading("Gb", text="GB")
        tree.heading("Percent", text="PERCENT")

        tree.column("Info", width=300, anchor="w")
        tree.column("Gb", width=200, anchor="center")
        tree.column("Percent", width=200, anchor="center")

        rows = [
            ("Free Memory", memory_data["memory_free"], memory_data["memory_free_percent"]),
            ("Used Memory", memory_data["memory_usage"], memory_data["memory_usage_percent"]),
            ("Free Virtual Memory", memory_data["vmem_free"], memory_data["vmem_free_percent"]),
        ]

        for row in rows:
            tree.insert("", "end", values=row)

    def static_data_table(self, static_data):
        table_frame = tk.Frame(self.root, bg="#dcdcdc")
        table_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        label = tk.Label(table_frame, text="Static Data", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, pady=(0, 5), sticky="w")

        columns = ("Info", "Gb", "Percent")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=2)
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
        table_frame = tk.Frame(self.root, bg="#dcdcdc")
        table_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        label = tk.Label(table_frame, text="Process X Threads", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, pady=(0, 5), sticky="w")

        columns = ("Info", "Numbers")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=2)
        tree.grid(row=1, column=0, sticky="nsew")

        tree.heading("Info", text=" ")
        tree.heading("Numbers", text="NUMBERS")

        tree.column("Info", width=300, anchor="w")
        tree.column("Numbers", width=200, anchor="center")

        rows = [
            ("Processes", len(process_threads_data)),
            ("Threads", n_threads),
        ]

        for row in rows:
            tree.insert("", "end", values=row)

    def show_process_table(self, processes_data):
        table_frame = tk.Frame(self.root, bg="#dcdcdc")
        table_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        label = tk.Label(table_frame, text="Processes Information", font=("Arial", 12, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, pady=(10, 5), sticky="w")

        inner_frame = tk.Frame(table_frame)
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

        tree = ttk.Treeview(inner_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)

        for col in columns:
            tree.heading(col, text=col.upper())
            tree.column(col, width=column_widths.get(col, 100), anchor="w")

        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        for process in processes_data:
            tree.insert("", "end", values=(
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


if __name__ == "__main__":
    root = tk.Tk()
    interface = Interface(root)
