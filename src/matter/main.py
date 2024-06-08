import docker
import re
import os 
import time
allTab = []

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
    tab = string.split(' ',5)
    if tab[4].startswith("[chip.native"):
        pass
    elif tab[4].startswith("[matter_server.server"):
        pass
    elif tab[4].startswith("[PersistentStorage]"):
        pass
    elif tab[4].startswith("[CertificateAuthority"):
        pass
    elif tab[4].startswith("[aiorun]"):
        pass
    elif tab[4].startswith("[asyncio]"):
        pass
    elif tab[4].startswith("[zeroconf]"):
        pass
    elif tab[4].startswith("[FabricAdmin]"):
        pass
    elif tab[4].startswith("[root]"):
        pass
    else:
        if tab[4] not in allTab:
            with open("file.txt", "a") as f:
                f.write(tab[4])

if __name__ == "__main__":
   stream_docker_logs('addon_core_matter_server')
