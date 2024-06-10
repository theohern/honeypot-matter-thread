import docker
import re
import os 
import time
import csv
from datetime import datetime
from parsing import matter_server
from parsing import chip
from parsing import storage

allTab = []

def TabInFile(file, tab, Skip=False):
    if Skip:
        with open("bin.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
        return
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(tab)

def initFile(file):
    with open(file, "w") as f:
        f.write("Date, Thread, Type, Source, Info\n")

def init():
    initFile("csv/allLogs.csv")
    initFile("csv/aiorun.csv")
    initFile("csv/asyncio.csv")
    initFile("csv/certif.csv")
    initFile("csv/chip.csv")
    initFile("csv/fabric.csv")
    initFile("csv/matter_server.csv")
    initFile("csv/pyWarnings.csv")
    initFile("csv/storage.csv")
    initFile("csv/zeroconf.csv")


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
    TabInFile("csv/allLogs.csv", tab)

    if tab[3].startswith("[chip.native"):
        with open("csv/chip.csv", "a") as fchip:
            writer = csv.writer(fchip)
            writer.writerow(tab)
        chip.parse(tab)
    elif tab[3].startswith("[matter_server.server"):
        with open("csv/matter_server.csv", "a") as fmatter:
            writer = csv.writer(fmatter)
            writer.writerow(tab)
        matter_server.parse(tab)
    elif tab[3].startswith("[PersistentStorage]"):
        with open("csv/storage.csv", "a") as fstor:
            writer = csv.writer(fstor)
            writer.writerow(tab)
        storage.parse(tab)
    elif tab[3].startswith("[CertificateAuthority"):
        with open("csv/certif.csv", "a") as fcert:
            writer = csv.writer(fcert)
            writer.writerow(tab)
    elif tab[3].startswith("[aiorun]"):
        with open("csv/aiorun.csv", "a") as faio:
            writer = csv.writer(faio)
            writer.writerow(tab)
    elif tab[3].startswith("[asyncio]"):
        with open("csv/asyncio.csv", "a") as fasyn:
            writer = csv.writer(fasyn)
            writer.writerow(tab)
    elif tab[3].startswith("[zeroconf]"):
        with open("csv/zeroconf.csv", "a") as fzer:
            writer = csv.writer(fzer)
            writer.writerow(tab)
    elif tab[3].startswith("[FabricAdmin]"):
        with open("csv/fabric.csv", "a") as ffab:
            writer = csv.writer(ffab)
            writer.writerow(tab)
    elif tab[3].startswith("[root]"):
        with open("csv/root.csv", "a") as froot:
            writer = csv.writer(froot)
            writer.writerow(tab)
    elif tab[3].startswith("[py.warnings]"):
        with open("csv/pyWarnings.csv", "a") as froot:
            writer = csv.writer(froot)
            writer.writerow(tab)
    else:
        if tab[3] not in allTab:
            with open("NotParse.txt", "a") as f:
                f.write(tab[3])

if __name__ == "__main__":
    init()
    stream_docker_logs('addon_core_matter_server')
