import re
import csv
import os

NP = " NOT PARSED"
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

def parse(tab):
    skip = False

    # Stack 
    if re.search(re.escape("stack"), tab[3]):
        if re.search(re.escape("CHIP Controller Stack initialized."), tab[4]):
           pass 
        else:
           tab[4] = tab[4] + NP 
        TabInFile(prefix+"resume.csv", tab)

    # SDK 
    elif re.search(re.escape("sdk"), tab[3]):
        # Initialization of device controller
        if re.search(re.escape("CASE"), tab[4]):
            pass
        elif re.search(re.escape("CHIP Device Controller Initialized"), tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP           
        TabInFile(prefix+"resume.csv", tab)

    # Helpers
    elif re.search(re.escape("helpers"), tab[3]):
        if re.search(r"[sS]kip", tab[4]):
            skip = True
        elif re.search(r"[fF]etch", tab[4]):
            skip = True
        elif re.search(r"[wW]riting", tab[4]):
            skip = True
        elif re.search(r"[dD]ownloading", tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # Storage
    elif re.search(re.escape("storage"), tab[3]):
        if re.search(re.escape("Loading persistent settings from"), tab[4]):
            pass
        elif re.search(re.escape("Started."), tab[4]):
            pass
        elif re.search(re.escape("Saved data to persistent storage"), tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab)

    # Vendor
    elif re.search(re.escape("vendor_info"), tab[3]):
        if re.search(re.escape("Loading vendor info from storage."), tab[4]):
            pass
        elif re.search(re.escape("Loaded 200 vendors from storage."), tab[4]):
            pass
        elif re.search(re.escape("Fetching the latest vendor info from DCL."), tab[4]):
            pass
        elif re.search(re.escape("Fetched 198 vendors from DCL."), tab[4]):
            pass
        elif re.search(re.escape("Saving vendor info to storage."), tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab)

    # Client Handler
    elif re.search(re.escape("client_handler"), tab[3]):
        if re.search(re.escape("Connected from"), tab[4]):
            pass
        elif re.search(re.escape("Received: {"), tab[4]):
            skip = True
        elif re.search(re.escape("Received CommandMessage("), tab[4]):
            pass
        elif re.search(re.escape("Handling command start_listening"), tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # Device Controller
    elif re.search(re.escape("device_controller"), tab[3]):
        if re.search(re.escape("Loaded 5 nodes from stored configuration"), tab[4]):
            pass
        elif re.search(r"Node \d+ discovered on MDNS", tab[4]):
            pass
        elif re.search(re.escape("Setting-up node..."), tab[4]):
            pass
        elif re.search(re.escape("Setting up attributes and events subscription."), tab[4]):
            pass
        elif re.search(re.escape("Subscription succeeded with report interval [0; 60]"), tab[4]):
            pass
        elif re.search(re.escape("Attribute updated:"), tab[4]):
            skip = True
        elif re.search(re.escape("Node could not be discovered on the network; returning cached IP's"), tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # Server
    elif re.search(re.escape(".server.server"), tab[3]):
        if re.search(re.escape("Starting the Matter Server"), tab[4]):
            pass
        elif re.search(re.escape("Webserver initialized"), tab[4]):
            pass
        elif re.search(re.escape("Detected dashboard files"), tab[4]):
            tab[4] = "dashboard files detected for the Matter Server"
        else:
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab)

    else :
        with open(prefix+"parsing/matter.txt", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
