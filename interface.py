import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# Criação da janela principal
root = tk.Tk()
root.title("Dashboard - Projeto A")
root.geometry("1000x600")

# Frame principal
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# --- Seção: (Virtual) Memory ---
frame_memory = tk.LabelFrame(main_frame, text="Memory", font=("Arial", 12, "bold"))
frame_memory.place(x=10, y=10, width=400, height=235)

tk.Label(frame_memory, text="Total Memory: x", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
tk.Label(frame_memory, text="Free Memory: x", fg="orange").pack(anchor="w")
tk.Label(frame_memory, text="Used Memory: x", fg="blue").pack(anchor="w")
tk.Label(frame_memory, text="Total Virtual Memory: x", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
tk.Label(frame_memory, text="Used Virtual Memory: x", fg="orange").pack(anchor="w")
tk.Label(frame_memory, text="Used Memory (%): x%", font=("Arial", 11), fg="green").pack(anchor="w")
tk.Label(frame_memory, text="Free Memory (%): x%", font=("Arial", 11), fg="green").pack(anchor="w")
tk.Label(frame_memory, text="Used Virtual Memory (%): x%", font=("Arial", 11), fg="green").pack(anchor="w")
tk.Label(frame_memory, text="Free Virtual Memory (%): x%", font=("Arial", 11), fg="green").pack(anchor="w")

# Iniciar app
root.mainloop()