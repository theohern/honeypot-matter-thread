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


class Message:
    def __init__(self, tab, on=False, size=0, skip=False, file="bin.csv"):
        self.tab = tab
        self.on = on
        self.size = size 
        self.skip = skip
        self.file = file
    
    def clear(self):
        self.tab = []
        self.size = 0
        self.on = False
        self.skip = False
        self.file = "bin.csv"

    def new(self,tab, file):
        self.tab = tab
        self.on = True
        self.file = file

    def close(self):
        TabInFile(self.file, self.tab, Skip=self.skip)
        self.clear()

    def skip(self):
        self.skip = True

    def add(self,string):
        self.tab[5] = self.tab[5] + string 
        self.size += 1

    def dec(self):
        self.size += 1

    def inc(self):
        self.size -= 1  

    def getOn(self):
        return self.on


Msg = Message([])

def parse(tab):
    skip = False
    # DMG Data Management 
    if re.search(re.escape("DMG"), tab[4]):
        if re.search("MoveToState ReadClient", tab[5]):
            pass
        elif re.search("SubscribeResponse is received", tab[5]):
            pass
        elif re.search("Subscription established with SubscriptionID", tab[5]):
            pass 
        elif re.search("SubscribeResponseMessage =", tab[5]):
            Msg.new(tab,"resume.csv")
            skip = True
        elif re.search("ReportDataMessage =", tab[5]):
            Msg.new(tab,"data/reportedDataMessage.csv")
            skip = True
        elif re.search(r"^}", tab[5]) and Msg.getOn():
            Msg.add(tab[5])
            Msg.close()
            skip = True
        elif Msg.getOn():
            Msg.add(tab[5])
            skip = True
        elif re.search("Refresh LivenessCheckTime", tab[5]):
            TabInFile("data/liveness.csv", tab)
            skip = True
        else :
            tab.append(NP)
        TabInFile("resume.csv", tab, Skip=skip)

    # EM Event Management
    elif re.search(re.escape("EM"), tab[4]):
        pass

    # IN Interaction
    elif re.search(re.escape("IN"), tab[4]):
        pass

    # SC Security
    elif re.search(re.escape("SC"), tab[4]):
        pass

    # ZCL Zigbee Cluster
    elif re.search(re.escape("ZCL"), tab[4]):
        pass

    # CTL Control
    elif re.search(re.escape("CTL"), tab[4]):
        pass

    # DL Data Layer 
    elif re.search(re.escape("DL"), tab[4]):
        pass

    # SPT Support
    elif re.search(re.escape("SPT"), tab[4]):
        pass

    # FP Fabric Provisioning
    elif re.search(re.escape("FP"), tab[4]):
        pass

    # TS Transport
    elif re.search(re.escape("TS"), tab[4]):
        pass

    # CSM Commissioning
    elif re.search(re.escape("CSM"), tab[4]):
        pass

    # DIS Discovery
    elif re.search(re.escape("DIS"), tab[4]):
        pass

    # IM Interaction Model
    elif re.search(re.escape("IM"), tab[4]):
        pass
    else :
        with open("parsing/chip.txt", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
