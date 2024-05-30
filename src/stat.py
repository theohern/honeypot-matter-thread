import docker
import csv
import time
import os
from datetime import datetime


def makeStat(csv_matter, csv_homeassistant):

    # Initialize Docker client
    client = docker.from_env()

    while True:
        # Get current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get Docker stats for the specified container
        matterStat = client.containers.get("addon_core_matter_server").stats(stream=False)
        homeassistantStat = client.containers.get("homeassistant").stats(stream=False)
        
        # Extract relevant stats
        cpuMatter = matterStat['cpu_stats']['cpu_usage']['total_usage'] / matterStat['cpu_stats']['system_cpu_usage'] * 100
        memoryMatter = matterStat['memory_stats']['usage'] / (1024 * 1024)  # Convert to MiB


        cpuHA = homeassistantStat['cpu_stats']['cpu_usage']['total_usage'] / homeassistantStat['cpu_stats']['system_cpu_usage'] * 100
        memoryHA = homeassistantStat['memory_stats']['usage'] / (1024 * 1024)  # Convert to MiB
        
        # Append stats to CSV file
        with open(csv_matter, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, f"{cpuMatter:.2f}", f"{matterStat['memory_stats']['usage']/1024/1024:.2f}", f"{memoryMatter:.2f}"])

        
        with open(csv_homeassistant, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, f"{cpuHA:.2f}", f"{homeassistantStat['memory_stats']['usage']/1024/1024:.2f}", f"{memoryHA:.2f}"])
        
        # Wait for 1 second
        time.sleep(1)

if __name__ == "__main__":

    
    # Define the path to the CSV file
    csv_matter = "/usr/share/grafana/csv/matter-stat.csv"
    
    csv_ha = "/usr/share/grafana/csv/homeassistant-stat.csv"

    if os.path.getsize(csv_matter) == 0:
        with open(csv_matter, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "CPU", "RAM", "Mem"])

    if os.path.getsize(csv_ha) == 0:

        with open(csv_ha, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "CPU", "RAM", "Mem"])

    makeStat(csv_matter, csv_ha)
