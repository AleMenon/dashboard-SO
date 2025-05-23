import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# Main window
root = tk.Tk()
root.title("Dashboard - Projeto A")

# ========== Frame: Operation System ==========
op_frame = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
op_frame.pack(side="top", fill="x")
tk.Label(op_frame, text="Operation System", font=("Arial", 16), fg="black").pack()

# ========== Frame: Pie Chart ==========
def pie_chart_memory(root, name, data_percent, x=0, y=0):
    chart_frame = tk.Frame(root)
    chart_frame.place(x=x, y=y)  # Usa coordenadas exatas

    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    labels = ['Free', 'Used']
    size_percent = [data_percent, 100.0 - data_percent]
    colors = ['green', 'red']
    ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
    ax.set_title(name)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# ========== Frame: Memory Table ==========
def show_memory_table(root, x=80, y=90):
    memory_frame = tk.Frame(root, bg="#dcdcdc")
    memory_frame.place(x=x, y=y)

    # Label centralizado sem adicionar altura extra
    label = tk.Label(memory_frame, text="Memory Information", font=("Arial", 14, "bold"), bg="#dcdcdc")
    label.grid(row=0, column=0, pady=(0, 5), sticky="w")

    # Treeview com colunas fixas
    columns = ("Info", "Gb", "Percent")
    tree = ttk.Treeview(memory_frame, columns=columns, show='headings', height=6)  # Define altura exata em linhas

    tree.grid(row=1, column=0, sticky="nsew")

    # Cabeçalhos
    tree.heading("Info", text=" ")
    tree.heading("Gb", text="GB")
    tree.heading("Percent", text="PERCENT")

    # Largura das colunas
    tree.column("Info", width=300, anchor="w")
    tree.column("Gb", width=200, anchor="center")
    tree.column("Percent", width=200, anchor="center")

    # Dados da tabela
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

    # Impede que o frame cresça além do necessário
    memory_frame.update_idletasks()
    memory_frame.config(height=tree.winfo_height() + label.winfo_height())

# ========== Frame: Process X Threads ==========
def show_process_and_threads_table(root, x=80, y=300):
    # Frame principal
    table_frame = tk.Frame(root, bg="#dcdcdc")
    table_frame.place(x=x, y=y)

    # Label
    label = tk.Label(table_frame, text="Process X Threads", font=("Arial", 14, "bold"), bg="#dcdcdc")
    label.pack(anchor="w", pady=(0, 5))

    # Treeview
    columns = ("Info", "Numbers")
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=2)  # Só 2 linhas, já ajustado

    # Cabeçalhos
    tree.heading("Info", text=" ")
    tree.heading("Numbers", text="NUMBERS")

    # Largura das colunas
    tree.column("Info", width=300, anchor="w")
    tree.column("Numbers", width=200, anchor="center")

    # Dados
    rows = [
        ("Processes", "X"),
        ("Threads", "X"),
    ]
    for row in rows:
        tree.insert("", "end", values=row)

    # Posiciona a tabela com pack e sem expandir além do necessário
    tree.pack()


# ========== Frame: Processes Table ==========
def show_process_table(root, x=80, y=600, width=900, height=300):
    # Frame principal
    table_frame = tk.Frame(root, width=width, height=height, bg="#dcdcdc")
    table_frame.place(x=x, y=y)

    # Título
    tk.Label(table_frame, text="Processes Information", font=("Arial", 12, "bold"), bg="#dcdcdc").pack(pady=(10, 5))

    # Frame interno para tabela e scrollbar
    inner_frame = tk.Frame(table_frame)
    inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbar vertical
    scrollbar = tk.Scrollbar(inner_frame)
    scrollbar.pack(side="right", fill="y")

    # Tabela (Treeview)
    columns = ("Process ID", "Name", "User", "CPU Used", "Memory Used", "Number of Threads")
    tree = ttk.Treeview(inner_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)

    # Configurações das colunas
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=270)

    tree.pack(fill="both", expand=True)

    # Conecta a scrollbar
    scrollbar.config(command=tree.yview)

    # Dados
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
        ("Process ID", "Name14", "User", "CPU Used", "Memory Used", "Number of Threads")
    ]

    for row in data:
        tree.insert("", "end", values=row)

# Uso no tkinter
if __name__ == "__main__":
    root.geometry("1800x700")
    root.configure(bg="#dcdcdc")
    show_process_table(root)
    pie_chart_memory(root, "Memory Status", 75.0, x=900, y=90)  # diferença entre os gráficos deve ser 300 para ficarem colados!
    pie_chart_memory(root, "Virtual Memory Status", 35.0, x=1200, y=90)
    pie_chart_memory(root, "CPU Status", 75.0, x=1500, y=90)
    show_memory_table(root)
    show_process_and_threads_table(root)
    root.mainloop()