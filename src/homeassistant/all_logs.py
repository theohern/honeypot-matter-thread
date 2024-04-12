import docker
import re

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
    good_match = re.search(r'\bhomeassistant\.core\b', log_entry)
    if good_match:
        SplitedLog = log_entry.split(' ', 5)
        data = []
        data.append(index)
        data.append(SplitedLog[0] + ' ' + SplitedLog[1].split(':', 2)[0] + ':' + SplitedLog[1].split(':', 2)[1] + ':00')
        data.append(SplitedLog[2])
        data.append(SplitedLog[3])
        data.append(SplitedLog[4])
        data.append(SplitedLog[5])
    
        with open("/usr/share/grafana/csv/ha_all_logs.csv", 'a') as f:
            f.write(ArrayToString(data)+'\n')

if __name__ == "__main__":
    with open("/usr/share/grafana/csv/ha_all_logs.csv", 'w') as f:
        f.write("ID\ttimestamp\tloglevel\tthread\tnamespace\tmessage\n")
    stream_docker_logs('homeassistant')