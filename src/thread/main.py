import docker
import re
import csv

index = 0

def ArrayToString(tab):
    string = ""
    for elem in tab :
        string = string + str(elem) + "\t"
    return string[:-1]

def stream_docker_logs(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    try:
        for log in container.logs(stream=True, follow=True):
            process_log_entry(log.decode('utf-8'))
    except KeyboardInterrupt:
        print("Script interrupted. Cleaning up...")
        print("Cleanup complete. Exiting script.")

def process_log_entry(log_entry):
    global index
    log_entry = re.sub(r'\x1B\[[0-9;]*m', '', log_entry)
    
    timestamp = log_entry[0:12].strip()
    data = [index, timestamp, log_entry.strip()]
    with open("/usr/share/grafana/csv/thread_logs.csv", 'w') as f:
        csv.writer(f).writerow(data)

    event_type = detect_event_type(log_entry)
    
    if event_type:
        device_name = extract_device_name(log_entry, event_type)
        data = [index, timestamp, device_name, event_type, log_entry.strip()]
        with open("/usr/share/grafana/csv/thread_nodes.csv", 'a') as f:
            csv.writer(f).writerow(data)
        index += 1

def detect_event_type(line):
    keywords = {
        "node_added": ["Successfully registered host"],
        "node_removed": ["Removed host"],
    }
    for event_type, kw_list in keywords.items():
        for keyword in kw_list:
            if keyword in line:
                return event_type
    return None

# Function to extract device name
def extract_device_name(line, event_type):
    if event_type == "node_added":
        match = re.search(r'Successfully registered host (\S+)', line)
        return match.group(1) if match else "Unknown"
    elif event_type == "node_removed":
        match = re.search(r'Removed host (\S+)', line)
        return match.group(1) if match else "Unknown"
    return "N/A"

if __name__ == "__main__":
    with open("/usr/share/grafana/csv/thread_nodes.csv", 'w') as f:
        csv.writer(f).writerow(['ID', 'Timestamp', 'Device Name', 'Event_Type', 'Log_Line'])
    with open("/usr/share/grafana/csv/thread_logs.csv", 'w') as f:
        csv.writer(f).writerow(['ID', 'Timestamp', 'Log_Line'])
    stream_docker_logs('addon_core_openthread_border_router')
