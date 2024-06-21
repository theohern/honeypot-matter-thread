import docker
import re
import os 
import time
import csv
from datetime import datetime
from parsing import matter_server
from parsing import chip

allTab = []
prefix = "/usr/share/grafana/csv/"

def TabInFile(file, tab, Skip=False):
    if Skip:
        with open(prefix+"bin.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
        return
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(tab)

def initFile(file):
    with open(file, "w") as f:
        f.write("Date, Thread, Type, Source, Info\n")

def initLogs():
    initFile(prefix+"matter/allLogs.csv")
    initFile(prefix+"matter/aiorun.csv")
    initFile(prefix+"matter/asyncio.csv")
    initFile(prefix+"matter/certif.csv")
    initFile(prefix+"matter/chip.csv")
    initFile(prefix+"matter/fabric.csv")
    initFile(prefix+"matter/matter_server.csv")
    initFile(prefix+"matter/pyWarnings.csv")
    initFile(prefix+"matter/storage.csv")
    initFile(prefix+"matter/zeroconf.csv")

def initCounts():
    with open(prefix+"matter/Source.csv", "w") as f:
        f.write("Name, Count\n")
    with open(prefix+"matter/Type.csv", "w") as f:
        f.write("Name, Count\n")
    with open(prefix+"matter/Thread.csv", "w") as f:
        f.write("Name, Count\n")
    

def UpdateInc(file, name):
    with open(file, mode='r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    verbose_exists = False
    for row in rows:
        if row[0] == name:
            row[1] = str(int(row[1]) + 1)
            verbose_exists = True
    if not verbose_exists:
        rows.append([name, "1"])

    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def stream_docker_logs(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    try:
        log_generator = container.logs(stream=True, follow=True)  # tail spécifie le nombre de lignes à retourner
        for _ in range(87):
            next(log_generator)
        # Traiter les logs restants
        for log in log_generator:
            date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
            if date_pattern.match(log.decode('utf-8')):
                process_log_entry(log.decode('utf-8'))
    except KeyboardInterrupt:
        print("Script interrupted. Cleaning up...")
        print("Cleanup complete. Exiting script.")

def process_log_entry(string):
    # parsing the string
    string = string.rstrip('\n')
    string = string.replace(",", ";")
    tab = string.split(' ',5)
    # change the date format
    milliOut = tab[1].split(".")[0]
    s = f"{tab[0]}T{milliOut}+01:00"
    tab = [s] + tab[2:]

    # add the log in allLogs file
    TabInFile(prefix+"matter/allLogs.csv", tab)

    # Update Source and Thread
    UpdateInc(prefix+"matter/Thread.csv", tab[1].replace("(","").replace(")",""))
    UpdateInc(prefix+"matter/Type.csv", tab[2])
    UpdateInc(prefix+"matter/Source.csv", tab[3].split(".")[0].replace("[", "").replace("]", ""))

    if tab[3].startswith("[chip.native"):
        with open(prefix+"matter/chip.csv", "a") as fchip:
            writer = csv.writer(fchip)
            writer.writerow(tab)
        chip.parse(tab)
    elif tab[3].startswith("[matter_server.server"):
        with open(prefix+"matter/matter_server.csv", "a") as fmatter:
            writer = csv.writer(fmatter)
            writer.writerow(tab)
        matter_server.parse(tab)
    elif tab[3].startswith("[PersistentStorage]"):
        with open(prefix+"matter/storage.csv", "a") as fstor:
            writer = csv.writer(fstor)
            writer.writerow(tab)
    elif tab[3].startswith("[CertificateAuthority"):
        with open(prefix+"matter/certif.csv", "a") as fcert:
            writer = csv.writer(fcert)
            writer.writerow(tab)
    elif tab[3].startswith("[aiorun]"):
        with open(prefix+"matter/aiorun.csv", "a") as faio:
            writer = csv.writer(faio)
            writer.writerow(tab)
    elif tab[3].startswith("[asyncio]"):
        with open(prefix+"matter/asyncio.csv", "a") as fasyn:
            writer = csv.writer(fasyn)
            writer.writerow(tab)
    elif tab[3].startswith("[zeroconf]"):
        with open(prefix+"matter/zeroconf.csv", "a") as fzer:
            writer = csv.writer(fzer)
            writer.writerow(tab)
    elif tab[3].startswith("[FabricAdmin]"):
        with open(prefix+"matter/fabric.csv", "a") as ffab:
            writer = csv.writer(ffab)
            writer.writerow(tab)
    elif tab[3].startswith("[root]"):
        with open(prefix+"matter/root.csv", "a") as froot:
            writer = csv.writer(froot)
            writer.writerow(tab)
    elif tab[3].startswith("[py.warnings]"):
        with open(prefix+"matter/pyWarnings.csv", "a") as froot:
            writer = csv.writer(froot)
            writer.writerow(tab)
    else:
        if tab[3] not in allTab:
            with open(prefix+"NotParse.txt", "a") as f:
                f.write(tab[3])

if __name__ == "__main__":
    initLogs()
    initCounts()
    stream_docker_logs('addon_core_matter_server')
