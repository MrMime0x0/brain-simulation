import sqlite3
import random
import time
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
def plot_activity(region, data):
    timestamps = [row[0] for row in data]
    neuron_ids = [row[1] for row in data]
    activity_levels = [row[2] for row in data]

    plt.figure(figsize=(10, 6))
    plt.scatter(timestamps, neuron_ids, c=activity_levels, cmap='viridis', marker='o')
    plt.colorbar(label='Activity Level')
    plt.title(f'{region.capitalize()} Neuron Activities')
    plt.xlabel('Time')
    plt.ylabel('Neuron ID')
    plt.show()

# Main function to execute the simulation and visualization
def main():
    create_tables()
    simulate_neurons('cerebrum', 100, 10, 0.1)  # Simulate 100 cerebrum neurons for 10 seconds
    simulate_neurons('cerebellum', 50, 10, 0.1)  # Simulate 50 cerebellum neurons for 10 seconds
    simulate_neurons('brainstem', 30, 10, 0.1)  # Simulate 30 brainstem neurons for 10 seconds

    cerebrum_data = retrieve_data('cerebrum')
    cerebellum_data = retrieve_data('cerebellum')
    brainstem_data = retrieve_data('brainstem')

    plot_activity('cerebrum', cerebrum_data)
    plot_activity('cerebellum', cerebellum_data)
    plot_activity('brainstem', brainstem_data)

if __name__ == "__main__":
    main()
