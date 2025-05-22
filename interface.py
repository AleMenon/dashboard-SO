import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

"""
# Criação da janela principal
root = tk.Tk()
root.title("Dashboard - Projeto A")
root.geometry("1000x600")

# Frame principal
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)
"""
# --- Seção: (Virtual) Memory ---
def memory_graphic(total_m, free_m, used_m, total_vm, used_vm, used_percent_m, free_percent_m, used_percent_vm, free_percent_vm):
    frame_memory = tk.LabelFrame(main_frame, text="Memory", font=("Arial", 12, "bold"))
    frame_memory.place(x=10, y=10, width=400, height=235)

    tk.Label(frame_memory, text=f"Total Memory: {total_m}", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
    tk.Label(frame_memory, text=f"Free Memory: {free_m}", fg="orange").pack(anchor="w")
    tk.Label(frame_memory, text=f"Used Memory: {used_m}", fg="blue").pack(anchor="w")
    tk.Label(frame_memory, text=f"Total Virtual Memory: {total_vm}", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
    tk.Label(frame_memory, text=f"Used Virtual Memory: {used_vm}", fg="orange").pack(anchor="w")
    tk.Label(frame_memory, text=f"Used Memory (%): {used_percent_m}%", font=("Arial", 11), fg="green").pack(anchor="w")
    tk.Label(frame_memory, text=f"Free Memory (%): {free_percent_m}%", font=("Arial", 11), fg="green").pack(anchor="w")
    tk.Label(frame_memory, text=f"Used Virtual Memory (%): {used_percent_vm}%", font=("Arial", 11), fg="green").pack(anchor="w")
    tk.Label(frame_memory, text=f"Free Virtual Memory (%): {free_percent_vm}%", font=("Arial", 11), fg="green").pack(anchor="w")

# memory_graphic(10,20,30,40,50,60,70,80,90)

# Iniciar app
#root.mainloop()