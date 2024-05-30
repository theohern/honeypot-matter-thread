import docker
import re
import os

def array_to_string(tab):
    return ','.join(map(str, tab))

def stream_docker_logs(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    try:
        log_generator = container.logs(stream=True, follow=True, tail=0)
        for log in log_generator:
            process_log_entry(log.decode('utf-8'))
    except KeyboardInterrupt:
        print("Script interrupted. Cleaning up...")
        print("Cleanup complete. Exiting script.")

def process_log_entry(log_entry):
    if re.search(r'[INFO]-MDNS----: Successfully registered host', log_entry):
        handle_node_activity(log_entry, "join")
    elif re.search(r'[INFO]-MDNS----: Removed host', log_entry):
        handle_node_activity(log_entry, "leave")
    all_logs(log_entry)

def all_logs(log_entry):
    data = log_entry.split(": ", 2)
    with open("/usr/share/grafana/csv/threadLogs.csv", "a") as file:
        file.write(array_to_string(data) + '\n')

def handle_node_activity(log_entry, activity_type):
    data = log_entry.split(': ', 2)
    if activity_type == "leave":
        match = re.search(r'Removed host ([\da-fA-F]+)', log_entry)
        if match:
            node_id = match.group(1)
            data.append(node_id)
            data.append("Node left")
        else:
            data.append("Unknown")
            data.append("Unknown")

    else:
        match = re.search(r'Successfully registered host ([\da-fA-F]+)', log_entry)
        if match:
            node_id = match.group(1)
            data.append(node_id)
            data.append("Node joined")
        else:
            data.append("unknown")
            data.append("unknown")
    
    with open("/usr/share/grafana/csv/thread_node_activity.csv", 'a') as file:
        file.write(array_to_string(data) + '\n')

if __name__ == "__main__":
    if os.path.isfile("/usr/share/grafana/csv/thread_node_activity.csv"):
      with open("/usr/share/grafana/csv/thread_node_activity.csv", 'w') as file:
        file.write('Agent, Thread ,Node ID,Activity\n')

    if os.path.isfile("/usr/share/grafana/csv/threadLogs.csv"):
      with open("/usr/share/grafana/csv/threadLogs.csv", 'w') as file:
        file.write('Agent , Info, Message\n')

    stream_docker_logs('addon_core_openthread_border_router')

