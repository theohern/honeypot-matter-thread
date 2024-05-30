import docker
import re
import os 
import time

def ArrayToString(tab):
    string = ""
    for elem in tab :
        string = string + str(elem) + ","
    return string[:-1]

def stream_docker_logs(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    try:
        log_generator = container.logs(stream=True, follow=True)  # tail spécifie le nombre de lignes à retourner
        for _ in range(87):
            next(log_generator)
        # Traiter les logs restants
        for log in log_generator:
            process_log_entry(log.decode('utf-8'))
    except KeyboardInterrupt:
        print("Script interrupted. Cleaning up...")
        print("Cleanup complete. Exiting script.")

def process_log_entry(log_entry):
    log_entry = log_entry.replace(",", ";")
    if re.search(r'matter_server\.server\.device_controller', log_entry):
        filter_node(log_entry)
    
    allLogs(log_entry)

def allLogs(log_entry):
    data = log_entry.split(" ", 5)
    if len(data) == 6:
        data = [data[0] + ' ' + data[1]] + data[2:]
        d = data[0].split(":")[:2]
        data[0] = d[0] + ":" + d[1]
        with open ("/usr/share/grafana/csv/matterLogs.csv", "a") as file:
            file.write(ArrayToString(data))

def filter_node(log_entry):
    SplitedLog = log_entry.split(' ', 5)
    data = []
    data.append(SplitedLog[0]+' '+SplitedLog[1]) # ajouter la date
    data.append(SplitedLog[2]) # ajouer current thread
    data.append(SplitedLog[3]) # ajouer type

    with open ("/usr/share/grafana/csv/node.csv", "r") as file:
        lines = file.readlines()

    if re.search(r'[Ss]ubscription', log_entry):

        ID = SplitedLog[4].split('_')[-1][:-1] # ajouter l'ID du node
        data.append(ID)

        newNode = True
        UpdateNode = True
        if len(lines) > int(ID) : # node ID already in the file
            node = lines[int(ID)][:-1].split(",")
            newNode = False
        elif len(lines) == int(ID) : # new node 
            node = [ID,0,0,0,0]
        else : # problem in the file, correction
            with open("/usr/share/grafana/csv/node.csv", "a") as f:
                for i in range (int(ID) - len(lines)):
                    f.write(str(i+len(lines))+",0,0,0,0\n")
            node = [ID,0,0,0,0]


        if re.search(r'succeeded', SplitedLog[5]): 
            data.append(0)
            data.append("Subscription succeeded")
            node[1] = int(node[1]) + 1

        elif re.search(r'failed', SplitedLog[5]): 
            data.append(1)
            data.append("Subscription failed")
            node[2] = int(node[2]) + 1

        else : 
            data.append(2)
            data.append(SplitedLog[5][:-1])
            UpdateNode = False

        with open("/usr/share/grafana/csv/subscription.csv", 'a') as f:
            f.write(ArrayToString(data)+'\n')
        
        if UpdateNode :
            with open("/usr/share/grafana/csv/node.csv", 'w') as f:
                if newNode: lines.append(ArrayToString(node)+'\n')
                else : lines[int(ID)] = ArrayToString(node)+'\n'
                for l in lines:
                    f.write(l)



if __name__ == "__main__":
    if os.path.isfile("/usr/share/grafana/csv/subscription.csv"):
        with open("/usr/share/grafana/csv/subscription.csv", 'w') as f:
            f.write('Time,Thead,Type,node,code,message\n')
            
    if os.path.isfile("/usr/share/grafana/csv/node.csv"):
        with open("/usr/share/grafana/csv/node.csv", 'w') as f:
            f.write('node,subscription succeeded,subscription failed,commisioning succeeded,commissiononig failed\n')

    if os.path.isfile("/usr/share/grafana/csv/matterLogs.csv"):
        with open("/usr/share/grafana/csv/matterLogs.csv", 'w') as f:
            f.write('Time,Thead,Type,node,message\n')
    stream_docker_logs('addon_core_matter_server')
