import re
import csv
import os

NP = "NOT PARSED"

def TabInFile(file, tab, Skip=False):
    if Skip:
        with open("bin.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
        return
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(tab)

def parse(tab):
    skip = False

    # Stack 
    if re.search(re.escape("stack"), tab[4]):
        if re.search(re.escape("CHIP Controller Stack initialized."), tab[5]):
           pass 
        else:
            tab.append(NP)
        TabInFile("resume.csv", tab)

    # SDK 
    elif re.search(re.escape("sdk"), tab[4]):
        # Initialization of device controller
        if re.search(re.escape("CASE"), tab[5]):
            pass
        elif re.search(re.escape("CHIP Device Controller Initialized"), tab[5]):
            pass
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab)

    # Helpers
    elif re.search(re.escape("helpers"), tab[4]):
        if re.search(r"[sS]kip", tab[5]):
            skip = True
        elif re.search(r"[fF]etch", tab[5]):
            skip = True
        elif re.search(r"[wW]riting", tab[5]):
            skip = True
        elif re.search(r"[dD]ownloading", tab[5]):
            skip = True
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab, Skip=skip)

    # Storage
    elif re.search(re.escape("storage"), tab[4]):
        if re.search(re.escape("Loading persistent settings from"), tab[5]):
            pass
        elif re.search(re.escape("Started."), tab[5]):
            pass
        elif re.search(re.escape("Saved data to persistent storage"), tab[5]):
            pass
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab)

    # Vendor
    elif re.search(re.escape("vendor_info"), tab[4]):
        if re.search(re.escape("Loading vendor info from storage."), tab[5]):
            pass
        elif re.search(re.escape("Loaded 200 vendors from storage."), tab[5]):
            pass
        elif re.search(re.escape("Fetching the latest vendor info from DCL."), tab[5]):
            pass
        elif re.search(re.escape("Fetched 198 vendors from DCL."), tab[5]):
            pass
        elif re.search(re.escape("Saving vendor info to storage."), tab[5]):
            pass
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab)

    # Client Handler
    elif re.search(re.escape("client_handler"), tab[4]):
        if re.search(re.escape("Connected from"), tab[5]):
            pass
        elif re.search(re.escape("Received: {"), tab[5]):
            skip = True
        elif re.search(re.escape("Received CommandMessage("), tab[5]):
            pass
        elif re.search(re.escape("Handling command start_listening"), tab[5]):
            pass
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab, Skip=skip)

    # Device Controller
    elif re.search(re.escape("device_controller"), tab[4]):
        if re.search(re.escape("Loaded 5 nodes from stored configuration"), tab[5]):
            pass
        elif re.search(r"Node \d+ discovered on MDNS", tab[5]):
            pass
        elif re.search(re.escape("Setting-up node..."), tab[5]):
            pass
        elif re.search(re.escape("Setting up attributes and events subscription."), tab[5]):
            pass
        elif re.search(re.escape("Subscription succeeded with report interval [0; 60]"), tab[5]):
            pass
        elif re.search(re.escape("Attribute updated:"), tab[5]):
            skip = True
        elif re.search(re.escape("Node could not be discovered on the network; returning cached IP's"), tab[5]):
            skip = True
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab, Skip=skip)

    # Server
    elif re.search(re.escape(".server.server"), tab[4]):
        if re.search(re.escape("Starting the Matter Server"), tab[5]):
            pass
        elif re.search(re.escape("Webserver initialized"), tab[5]):
            pass
        elif re.search(re.escape("Detected dashboard files"), tab[5]):
            tab[5] = "dashboard files detected for the Matter Server"
        else:
            tab.append(NP)
        TabInFile("resume.csv", tab)

    else :
        with open("parsing/matter.txt", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
