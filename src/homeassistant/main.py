from flask import Flask, send_file
import docker
import re

app = Flask(__name__)

def stream_docker_logs(container_name):
    client = docker.from_env()
    change_counts = {}
    container = client.containers.get(container_name)
    try:
        for log in container.logs(stream=True, follow=True):
            process_log_entry(log.decode('utf-8'), change_counts)
    except KeyboardInterrupt:
        print("Script interrupted. Cleaning up...")
        save_change_counts_to_file(change_counts)
        print("Cleanup complete. Exiting script.")

def process_log_entry(log_entry, change_counts):
    match = re.search(r'friendly_name=([^@,]+)', log_entry)
    if match:
        old_state_match = re.search(r'old_state=<state [^=]+=([^;]+);', log_entry)
        old_state = old_state_match.group(1) if old_state_match else None
        new_state_match = re.search(r'new_state=<state [^=]+=([^;]+);', log_entry)
        new_state = new_state_match.group(1) if new_state_match else None
        state_changed = old_state != new_state
        
        count_changes(log_entry, change_counts, state_changed)
        save_change_counts_to_file(change_counts)

def count_changes(log_entry, change_counts, state_changed):
    if state_changed:
        friendly_name = re.search(r'friendly_name=([^@,]+)', log_entry).group(1).strip()
        change_counts[friendly_name] = change_counts.get(friendly_name, 0) + 1
    else:
        friendly_name = re.search(r'friendly_name=([^@,]+)', log_entry).group(1).strip()
        change_counts[f"{friendly_name}_minor_change"] = change_counts.get(f"{friendly_name}_minor_change", 0) + 1

def save_change_counts_to_file(change_counts):
    with open("csv/count_changes.csv", 'w') as f:
        f.write("Friendly Name,Change Count\n")
        for friendly_name, count in change_counts.items():
            f.write(f"{friendly_name},{count}\n")

@app.route('/get_homeassistant')
def get_csv():
    return send_file("csv/count_changes.csv", as_attachment=True)

if __name__ == "__main__":
    stream_docker_logs('homeassistant')
