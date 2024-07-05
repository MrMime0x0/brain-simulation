import sqlite3
import random
import time
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Step 1: Create database tables
def create_tables():
    conn = sqlite3.connect('brain_activity.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cerebrum
                 (timestamp REAL, neuron_id INTEGER, activity_level REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS cerebellum
                 (timestamp REAL, neuron_id INTEGER, activity_level REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS brainstem
                 (timestamp REAL, neuron_id INTEGER, activity_level REAL)''')
    conn.commit()
    conn.close()

# Step 2: Log activity to the database
def log_activity(region, neuron_id, activity_level):
    conn = sqlite3.connect('brain_activity.db')
    c = conn.cursor()
    c.execute(f'''INSERT INTO {region} (timestamp, neuron_id, activity_level)
                  VALUES (?, ?, ?)''', (time.time(), neuron_id, activity_level))
    conn.commit()
    conn.close()

# Step 3: Simulate neuron activities
def simulate_neurons(region, neuron_count, duration, interval):
    start_time = time.time()
    while time.time() - start_time < duration:
        for neuron_id in range(neuron_count):
            activity_level = random.random()
            log_activity(region, neuron_id, activity_level)
        time.sleep(interval)

# Step 4: Retrieve data from the database
def retrieve_data(region):
    conn = sqlite3.connect('brain_activity.db')
    c = conn.cursor()
    c.execute(f'''SELECT * FROM {region}''')
    data = c.fetchall()
    conn.close()
    return data

# Step 5: Plot the activity using Matplotlib
def plot_activity(region, data, ax, canvas):
    timestamps = [row[0] for row in data]
    neuron_ids = [row[1] for row in data]
    activity_levels = [row[2] for row in data]

    ax.clear()
    scatter = ax.scatter(timestamps, neuron_ids, c=activity_levels, cmap='viridis', marker='o')
    plt.colorbar(scatter, ax=ax, label='Activity Level')
    ax.set_title(f'{region.capitalize()} Neuron Activities')
    ax.set_xlabel('Time')
    ax.set_ylabel('Neuron ID')
    canvas.draw()

# GUI class to manage the application
class BrainActivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Activity Simulation")
        self.region = tk.StringVar(value='cerebrum')
        self.neuron_count = tk.IntVar(value=100)
        self.duration = tk.IntVar(value=10)
        self.interval = tk.DoubleVar(value=0.1)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Region:").grid(column=0, row=0, padx=10, pady=5)
        ttk.Combobox(self.root, textvariable=self.region, values=['cerebrum', 'cerebellum', 'brainstem']).grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(self.root, text="Neuron Count:").grid(column=0, row=1, padx=10, pady=5)
        ttk.Entry(self.root, textvariable=self.neuron_count).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self.root, text="Duration (s):").grid(column=0, row=2, padx=10, pady=5)
        ttk.Entry(self.root, textvariable=self.duration).grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.root, text="Interval (s):").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self.root, textvariable=self.interval).grid(column=1, row=3, padx=10, pady=5)

        self.start_button = ttk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Simulation", command=self.stop_simulation, state='disabled')
        self.stop_button.grid(column=0, row=5, columnspan=2, pady=10)

        self.plot_button = ttk.Button(self.root, text="Plot Activity", command=self.plot_activity)
        self.plot_button.grid(column=0, row=6, columnspan=2, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(column=0, row=7, columnspan=2)

        self.simulation_thread = None
        self.simulation_running = False

    def start_simulation(self):
        if self.simulation_thread is None or not self.simulation_thread.is_alive():
            self.simulation_running = True
            self.simulation_thread = threading.Thread(target=self.run_simulation)
            self.simulation_thread.start()
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')

    def stop_simulation(self):
        self.simulation_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def run_simulation(self):
        create_tables()
        simulate_neurons(self.region.get(), self.neuron_count.get(), self.duration.get(), self.interval.get())
        self.simulation_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def plot_activity(self):
        data = retrieve_data(self.region.get())
        plot_activity(self.region.get(), data, self.ax, self.canvas)

# Main function to execute the GUI application
def main():
    root = tk.Tk()
    app = BrainActivityApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
