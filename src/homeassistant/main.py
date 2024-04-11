import docker
import re

def ArrayToString(tab):
    string = ""
    for elem in tab :
        string = string + str(elem) + "\t"
    return string[:-1]

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
    log_entry = re.sub(r'\x1B\[[0-9;]*m', '', log_entry)
    match = re.search(r'friendly_name=([^@,]+)', log_entry)
    if match:
        good_match = re.search(r'\bhomeassistant\.core\b', log_entry)
        if good_match:
            SplitedLog = log_entry.split(' ', 5)
            data = []
            friendly_name = match.group(1).strip()
            data.append(friendly_name)
            data.append(SplitedLog[0] + ' ' + SplitedLog[1].split(':', 2)[0] + ':' + SplitedLog[1].split(':', 2)[1])
            data.append(SplitedLog[2])
            data.append(SplitedLog[3])
            data.append(SplitedLog[4])
            data.append(SplitedLog[5])
            
            old_state_match = re.search(r'old_state=<state [^=]+=([^;]+);', log_entry)
            old_state = old_state_match.group(1) if old_state_match else None
            new_state_match = re.search(r'new_state=<state [^=]+=([^;]+);', log_entry)
            new_state = new_state_match.group(1) if new_state_match else None
            state_changed = old_state != new_state
            
            count_changes(log_entry, change_counts, state_changed, data)
            save_change_counts_to_file(change_counts)

def count_changes(log_entry, change_counts, state_changed, data):
    excluded_words = ["Sun", "theophile", "Ledoug", "SM-A137F", "Google", "achats"]

    friendly_name_match = re.search(r'friendly_name=([^@,]+)', log_entry)
    if friendly_name_match:
        friendly_name = friendly_name_match.group(1).strip()

    if any(word in friendly_name for word in excluded_words):
            return
    
    with open("/usr/share/grafana/csv/ha_log_entries.csv", 'a') as f:
            f.write(ArrayToString(data)+'\n')
    if state_changed:
        change_counts[friendly_name] = change_counts.get(friendly_name, 0) + 1
    else:
        change_counts[f"{friendly_name}_minor_change"] = change_counts.get(f"{friendly_name}_minor_change", 0) + 1

def save_change_counts_to_file(change_counts):
    with open("/usr/share/grafana/csv/count_changes.csv", 'w') as f:
        f.write("Friendly Name,Change Count\n")
        for friendly_name, count in change_counts.items():
            f.write(f"{friendly_name},{count}\n")

if __name__ == "__main__":
    with open("/usr/share/grafana/csv/ha_log_entries.csv", 'w') as f:
        f.write("Friendly Name\ttimestamp\tloglevel\tthread\tnamespace\tmessage\n")
    stream_docker_logs('homeassistant')