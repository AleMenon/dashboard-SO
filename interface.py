import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

"""
Esta classe é responsável por construir e gerenciar todos os elementos da interface gráfica do dashboard.
Ela organiza os gráficos, tabelas e outros widgets para exibir informações de monitoramento do sistema.
"""
class Interface(tk.Frame):

    def __init__(self, parent, controller, data_collector):
        super().__init__(parent, bg="#dcdcdc")

        self.controller = controller
        self.data_collector = data_collector

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

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
        self.tablept_tree = None
        self.process_tree = None

        self.process_details_map = {}


        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

        self.create_op_frame()

    """
    Cria e posiciona o frame que contém o título principal "Sistema Operacional"
    na parte superior da janela do dashboard.
    """
    def create_op_frame(self):
        op_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=10)
        op_frame.grid(row=0, column=0, columnspan=3, sticky="new", padx=50, pady=10)

        op_frame.grid_columnconfigure(0, weight=1)
        op_frame.grid_columnconfigure(1, weight=0)

        label = tk.Label(op_frame, text="Sistema Operacional", font=("Arial", 16), fg="black")
        label.pack(anchor="center")

        switch_btn = tk.Button(op_frame, text="Arquivos",
                               command=lambda: self.controller.show_frame("FileFrame"))
        switch_btn.pack(side="right")

    """
    Cria ou atualiza um gráfico de pizza que exibe o status de uso da memória RAM (livre vs. usada).
    """
    def pie_chart_memory(self, data_memory):
        data_percent = data_memory["memory_free_percent"]

        if self.memory_chart_frame is None:
            self.memory_chart_frame = tk.Frame(self)
            self.memory_chart_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

            self.memory_fig, self.memory_ax = plt.subplots(figsize=(3.5, 3.5))
            self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=self.memory_chart_frame)
            self.memory_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.memory_ax.clear()
        labels = ['Livre', 'Usado']
        size_percent = [data_percent, 100 - data_percent]
        colors = ['green', 'red']
        self.memory_ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        self.memory_ax.set_title("Status da Memória")
        self.memory_canvas.draw()

    """
    Cria ou atualiza um gráfico de pizza que exibe o status de uso da memória virtual (livre vs. usada).
    """
    def pie_chart_virtual_memory(self, data_virtual_memory):
        data_percent = data_virtual_memory["vmem_free_percent"]

        if self.virtual_memory_chart_frame is None:
            self.virtual_memory_chart_frame = tk.Frame(self)
            self.virtual_memory_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            self.virtual_memory_fig, self.virtual_memory_ax = plt.subplots(figsize=(3.5, 3.5))
            self.virtual_memory_canvas = FigureCanvasTkAgg(self.virtual_memory_fig, master=self.virtual_memory_chart_frame)
            self.virtual_memory_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.virtual_memory_ax.clear()
        labels = ['livre', 'Usado']
        size_percent = [data_percent, 100 - data_percent]
        colors = ['green', 'red']
        self.virtual_memory_ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        self.virtual_memory_ax.set_title("Status da Memória Virtual")
        self.virtual_memory_canvas.draw()

    """
    Cria ou atualiza um gráfico de pizza que exibe o status de uso da CPU (ociosa vs. usada).
    """
    def pie_chart_cpu(self, data_cpu):
        data_percent = data_cpu["cpu_idle_percent"]

        if self.cpu_chart_frame is None:
            self.cpu_chart_frame = tk.Frame(self)
            self.cpu_chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.cpu_fig, self.cpu_ax = plt.subplots(figsize=(3.5, 3.5))
            self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_chart_frame)
            self.cpu_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.cpu_ax.clear()
        labels = ['Livre', 'Usado']
        size_percent = [data_percent, 100.0 - data_percent]
        colors = ['green', 'red']
        self.cpu_ax.pie(size_percent, labels=labels, colors=colors, autopct='%1.1f%%')
        self.cpu_ax.set_title("Status da CPU")
        self.cpu_canvas.draw()

    """
    Cria ou atualiza uma tabela que exibe informações dinâmicas de memória,
    como memória livre, usada e memória virtual livre, em GB e porcentagem.
    """
    def dinamic_data_table(self, memory_data):
        if self.memory_frame is None:
            self.memory_frame = tk.Frame(self, bg="#dcdcdc")
            self.memory_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.memory_frame, text="Informações Dinâmicas", font=("Arial", 14, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, pady=(0, 5), sticky="w")

            columns = ("Info", "Gb", "Porcentagem")
            self.memory_tree = ttk.Treeview(self.memory_frame, columns=columns, show='headings', height=3)
            self.memory_tree.grid(row=1, column=0, sticky="nsew")

            self.memory_tree.heading("Info", text=" ")
            self.memory_tree.heading("Gb", text="GB")
            self.memory_tree.heading("Porcentagem", text="PORCENTAGEM")

            self.memory_tree.column("Info", anchor="w", stretch=True)
            self.memory_tree.column("Gb", anchor="center", stretch=True)
            self.memory_tree.column("Porcentagem", anchor="center", stretch=True)
            self.memory_frame.bind("<Configure>", self.resize_memory_columns)


        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)


        rows = [
            ("Memória Livre", memory_data["memory_free"], memory_data["memory_free_percent"]),
            ("Memória Usada", memory_data["memory_usage"], memory_data["memory_usage_percent"]),
            ("memória Virtual Livre", memory_data["vmem_free"], memory_data["vmem_free_percent"]),
        ]

        for row in rows:
            self.memory_tree.insert("", "end", values=row)

    def resize_memory_columns(self, event):
        total_width = event.width
        self.memory_tree.column("Info", width=int(total_width * 0.5))
        self.memory_tree.column("Gb", width=int(total_width * 0.25))
        self.memory_tree.column("Porcentagem", width=int(total_width * 0.25))

    """
    Cria uma tabela que exibe informações estáticas de memória, como memória total
    e memória virtual total. Esta tabela é criada apenas uma vez, já que seus dados são estáticos.
    """
    def static_data_table(self, static_data):

        static_data_frame = tk.Frame(self, bg="#dcdcdc")
        static_data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        label = tk.Label(static_data_frame, text="Informações Estáticas", font=("Arial", 14, "bold"), bg="#dcdcdc")
        label.grid(row=0, column=0, pady=(0, 5), sticky="w")

        columns = ("Info", "Gb", "Porcentagem")
        tree = ttk.Treeview(static_data_frame, columns=columns, show='headings', height=3)
        tree.grid(row=1, column=0, sticky="nsew")

        tree.heading("Info", text=" ")
        tree.heading("Gb", text="GB")
        tree.heading("Porcentagem", text="PORCENTAGEM")

        tree.column("Info", anchor="w", stretch=True)
        tree.column("Gb", anchor="center", stretch=True)
        tree.column("Porcentagem", anchor="center", stretch=True)

        self.static_tree = tree  # Salva como atributo para usar no resize

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
        self.static_tree.column("Info", width=int(total_width * 0.5))
        self.static_tree.column("Gb", width=int(total_width * 0.25))
        self.static_tree.column("Porcentagem", width=int(total_width * 0.25))

    """
    Cria ou atualiza uma tabela com o número total de processos e threads em execução.
    """
    def show_process_and_threads_table(self, process_threads_data, n_threads):
        if self.tablept_frame is None:
            self.tablept_frame = tk.Frame(self, bg="#dcdcdc")
            self.tablept_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.tablept_frame, text="Processos X Threads", font=("Arial", 14, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, pady=(0, 5), sticky="w")

            columns = ("Info", "Números")
            self.tablept_tree = ttk.Treeview(self.tablept_frame, columns=columns, show='headings', height=2)
            self.tablept_tree.grid(row=1, column=0, sticky="nsew")

            self.tablept_tree.heading("Info", text=" ")
            self.tablept_tree.heading("Números", text="NÚMEROS")

            self.tablept_tree.column("Info", anchor="w", stretch=True)
            self.tablept_tree.column("Números", anchor="center", stretch=True)


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
        self.tablept_tree.column("Info", width=int(total_width * 0.7))
        self.tablept_tree.column("Números", width=int(total_width * 0.3))

    """
    Cria ou atualiza uma tabela detalhada listando todos os processos em
    execução com informações como ID, nome, usuário, uso de memória, etc.
    """

    def show_process_table(self, processes_data):
        if self.tablep_frame is None:
            self.tablep_frame = tk.Frame(self, bg="#dcdcdc")
            self.tablep_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

            label = tk.Label(self.tablep_frame, text="Informações dos Processos",
                             font=("Arial", 12, "bold"), bg="#dcdcdc")
            label.grid(row=0, column=0, pady=(10, 5), sticky="w")

            inner_frame = tk.Frame(self.tablep_frame)
            inner_frame.grid(row=1, column=0, sticky="nsew")

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
            self.process_tree.column(col, width=int(total_width * ratio))

    """
    Manipulador do evento de clique duplo em um item da tabela de processos.
    Quando o usuário clica duas vezes em uma linha, obtém os detalhes do processo
    correspondente e abre uma janela (popup) com informações adicionais.
    """

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

    """
    Abre uma nova janela (popup) para exibir os detalhes completos do processo selecionado,
    incluindo lista de threads associadas e recursos como arquivos abertos, bibliotecas,
    sockets, entre outros.
    """

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

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="Threads:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        for thread in process_info["thread_data"]:
            tk.Label(scrollable_frame, text=f"- {thread}", bg="#f0f0f0").pack(anchor="w", padx=20)

        tk.Label(scrollable_frame, text="\nRecursos:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        for k, v in process_info["resources"].items():
            tk.Label(scrollable_frame, text=f"{k.upper()} ({len(v)})", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(
                anchor="w")
            for item in v:
                tk.Label(scrollable_frame, text=f" - {item}", bg="#f0f0f0").pack(anchor="w", padx=20)

        tk.Button(popup, text="Fechar", command=popup.destroy).pack(pady=10)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    """
    Função de para atualizar o gráfico de status da CPU.
    """
    def update_data_cpu(self, data):
        self.pie_chart_cpu(data)

    """
    Função de para atualizar os gráficos de status de memória
    (RAM e virtual) e a tabela de informações dinâmicas de memória.
    """
    def update_data_memory(self, data):
        self.pie_chart_memory(data)
        self.pie_chart_virtual_memory(data)
        self.dinamic_data_table(data)

    """
    Função de conveniência para atualizar as tabelas de processos (detalhada e resumida).
    """
    def update_data_process(self, process, n_threads):
        self.show_process_table(process)
        self.show_process_and_threads_table(process, n_threads)