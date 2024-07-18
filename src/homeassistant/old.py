import docker
import re
import csv
from parsing import matter_server
from parsing import chip

allTab = []
prefix = "/usr/share/grafana/csv/"

def TabInFile(file, tab, Skip=False):
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(tab)
    if Skip:
        with open(prefix + "ha_bin.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)

def initFile(file):
    with open(file, "w") as f:
        f.write("Date, Thread, Type, Source, Info\n")

def initLogs():
    log_files = [
        "homeassistant/allLogs.csv",
        "homeassistant/aiorun.csv",
        "homeassistant/asyncio.csv",
        "homeassistant/certif.csv",
        "homeassistant/chip.csv",
        "homeassistant/fabric.csv",
        "homeassistant/matter_server.csv",
        "homeassistant/pyWarnings.csv",
        "homeassistant/storage.csv",
        "homeassistant/zeroconf.csv"
    ]
    for file in log_files:
        initFile(prefix + file)
 
def initCounts():
    count_files = ["homeassistant/Source.csv", "homeassistant/Type.csv", "homeassistant/Thread.csv"]
    for file in count_files:
        with open(prefix + file, "w") as f:
            f.write("Name, Count\n")

def UpdateInc(file, name):
    with open(file, mode='r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    updated = False
    for row in rows:
        if row[0] == name:
            row[1] = str(int(row[1]) + 1)
            updated = True
            break
    if not updated:
        rows.append([name, "1"])

    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def stream_docker_logs(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    try:
        log_generator = container.logs(stream=True, follow=True)
        for _ in range(87):
            next(log_generator)
        for log in log_generator:
            if log:
                date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
                if date_pattern.match(log.decode('utf-8')):
                    process_log_entry(log.decode('utf-8'))
    except KeyboardInterrupt:
        print("Script interrupted. Cleaning up...")
        print("Cleanup complete. Exiting script.")

def process_log_entry(string):
    string = string.rstrip('\n').replace(",", ";")
    tab = string.split(' ', 5)
    milliOut = ta  &b[1].split(".")[0]
    s = f"{tab[0]}T{milliOut}+01:00"
    tab = [s] + tab[2:]

    TabInFile(prefix + "homeassistant/allLogs.csv", tab)

    UpdateInc(prefix + "homeassistant/Thread.csv", tab[1].replace("(", "").replace(")", ""))
    UpdateInc(prefix + "homeassistant/Type.csv", tab[2])
    UpdateInc(prefix + "homeassistant/Source.csv", tab[3].split(".")[0].replace("[", "").replace("]", ""))

    log_mapping = {
        "[chip.native": "chip.csv",
        "[matter_server.server": "matter_server.csv",
        "[PersistentStorage]": "storage.csv",
        "[CertificateAuthority": "certif.csv",
        "[aiorun]": "aiorun.csv",
        "[asyncio]": "asyncio.csv",
        "[zeroconf]": "zeroconf.csv",
        "[FabricAdmin]": "fabric.csv",
        "[root]": "root.csv",
        "[py.warnings]": "pyWarnings.csv"
    }

    for key, file in log_mapping.items():
        if tab[3].startswith(key):
            TabInFile(prefix + f"homeassistant/{file}", tab)
            if "chip" in file:
                chip.parse(tab)
            elif "matter_server" in file:
                matter_server.parse(tab)
            break
    else:
        if tab[3] not in allTab:
            allTab.append(tab[3])
            with open(prefix + "Ha_NotParse.txt", "a") as f:
                f.write(tab[3] + "\n")

if __name__ == "__main__":
    initLogs()
    initCounts()
    stream_docker_logs('homeassistant')
