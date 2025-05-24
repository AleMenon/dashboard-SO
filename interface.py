import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Projeto A")
        self.root.geometry("1800x700")
        self.root.configure(bg="#dcdcdc")

        self.create_op_frame()
        self.show_process_table()
        self.pie_chart_memory("Memory Status", 75.0, x=900, y=90)
        self.pie_chart_memory("Virtual Memory Status", 35.0, x=1200, y=90)
        self.pie_chart_memory("CPU Status", 75.0, x=1500, y=90)
        self.show_memory_table()
        self.show_process_and_threads_table()

    def create_op_frame(self):
        op_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        op_frame.pack(side="top", fill="x")
        tk.Label(op_frame, text="Operation System", font=("Arial", 16), fg="black").pack()

    def pie_chart_memory(self, name, data_percent, x=0, y=0):
        chart_frame = tk.Frame(self.root)
        chart_frame.place(x=x, y=y)

        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        labels = ['Free', 'Used']
        size_percent = [data_percent, 100.0 - data_percent]
        colors = ['green', 'red']
        ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title(name)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_memory_table(self, x=80, y=90):
        memory_frame = tk.Frame(self.root, bg="#dcdcdc")
        memory_frame.place(x=x, y=y)

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
            ("Total Memory", "X KB", "X"),
            ("Free Memory", "X KB", "X"),
            ("Used Memory", "X KB", "X"),
            ("Total Swap", "X KB", "X"),
            ("Total Virtual Memory", "X KB", "X"),
            ("Free Virtual Memory", "X KB", "X"),
        ]

        for row in rows:
            tree.insert("", "end", values=row)

        memory_frame.update_idletasks()
        memory_frame.config(height=tree.winfo_height() + label.winfo_height())

    def show_process_and_threads_table(self, x=80, y=300):
        table_frame = tk.Frame(self.root, bg="#dcdcdc")
        table_frame.place(x=x, y=y)

        label = tk.Label(table_frame, text="Process X Threads", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.pack(anchor="w", pady=(0, 5))

        columns = ("Info", "Numbers")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=2)

        tree.heading("Info", text=" ")
        tree.heading("Numbers", text="NUMBERS")

        tree.column("Info", width=300, anchor="w")
        tree.column("Numbers", width=200, anchor="center")

        rows = [
            ("Processes", "X"),
            ("Threads", "X"),
        ]

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack()

    def show_process_table(self, x=80, y=600, width=900, height=300):
        table_frame = tk.Frame(self.root, width=width, height=height, bg="#dcdcdc")
        table_frame.place(x=x, y=y)

        tk.Label(table_frame, text="Processes Information", font=("Arial", 12, "bold"), bg="#dcdcdc").pack(pady=(10, 5))

        inner_frame = tk.Frame(table_frame)
        inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(inner_frame)
        scrollbar.pack(side="right", fill="y")

        columns = ("Process ID", "Name", "User", "CPU Used", "Memory Used", "Number of Threads")
        tree = ttk.Treeview(inner_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)

        for col in columns:
            tree.heading(col, text=col.upper())
            tree.column(col, width=270)

        tree.pack(fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        data = [
            ("Process ID", "Name1", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name2", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name3", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name4", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name5", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name6", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name7", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name8", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name9", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name10", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name11", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name12", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name13", "User", "CPU Used", "Memory Used", "Number of Threads"),
            ("Process ID", "Name14", "User", "CPU Used", "Memory Used", "Number of Threads"),
        ]

        for row in data:
            tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    interface = Interface(root)
    root.mainloop()
