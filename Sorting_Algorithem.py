import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sorting Algorithm (Bubble Sort with visualization)
def bubble_sort_visual(arr, bars):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Swap
                swapped = True
                update_bars(arr, bars)
                time.sleep(0.1)  # Delay for visualization
        if not swapped:
            break  # Optimization

# Function to update the bar chart
def update_bars(arr, bars):
    for bar, val in zip(bars, arr):
        bar.set_height(val)
    canvas.draw()
    root.update()

# Function to generate random numbers
def generate_numbers():
    global numbers, bars
    numbers = [random.randint(10, 100) for _ in range(20)]
    ax.clear()
    bars = ax.bar(range(len(numbers)), numbers, color='blue')
    canvas.draw()

# Function to start sorting
def start_sorting():
    bubble_sort_visual(numbers, bars)

# Create GUI window
root = tk.Tk()
root.title("Sorting Algorithm Visualizer")
root.geometry("600x500")

# Create Matplotlib figure
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

generate_btn = ttk.Button(btn_frame, text="Generate Numbers", command=generate_numbers)
generate_btn.grid(row=0, column=0, padx=10, pady=10)

sort_btn = ttk.Button(btn_frame, text="Start Sorting", command=start_sorting)
sort_btn.grid(row=0, column=1, padx=10, pady=10)

# Initial random numbers
numbers = []
bars = []
generate_numbers()

# Run the GUI
root.mainloop()
