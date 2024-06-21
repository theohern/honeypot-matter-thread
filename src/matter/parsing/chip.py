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


class Message:
    def __init__(self, tab, on=False, size=0, skip=False, file=prefix+"bin.csv"):
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
        self.file = prefix+"bin.csv"

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
        self.tab[4] = self.tab[4] + string 
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
    if re.search(re.escape("DMG"), tab[3]):
        if re.search("MoveToState ReadClient", tab[4]):
            pass
        elif re.search("SubscribeResponse is received", tab[4]):
            pass
        elif re.search("Subscription established with SubscriptionID", tab[4]):
            pass 
        elif re.search("SubscribeResponseMessage =", tab[4]):
            Msg.new(tab,prefix+"resume.csv")
            skip = True
        elif re.search("ReportDataMessage =", tab[4]):
            Msg.new(tab,prefix+"data/reportedDataMessage.csv")
            skip = True
        elif re.search(r"^}", tab[4]) and Msg.getOn():
            Msg.add(tab[4])
            Msg.close()
            skip = True
        elif Msg.getOn():
            Msg.add(tab[4])
            skip = True
        elif re.search("Refresh LivenessCheckTime", tab[4]):
            TabInFile("data/liveness.csv", tab)
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # EM Event Management
    elif re.search(re.escape("EM"), tab[3]):
        if re.search(r"^<<<", tab[4]):
            skip = True
        elif re.search(r"^>>>", tab[4]):
            skip = True
        elif re.search(r"^Found matching exchange:", tab[4]):
            skip = True
        elif re.search(r"^Rxd Ack; Removing MessageCounter:", tab[4]):
            skip = True
        elif re.search(r"^Handling via exchange:", tab[4]):
            skip = True
        elif re.search(r"^Flushed pending ack for MessageCounter:", tab[4]):
            skip = True
        elif re.search(r"^CHIP MessageCounter:", tab[4]):
            skip = True
        elif re.search(r"^Retransmitting MessageCounter:", tab[4]):
            skip = True
        elif re.search(r"^Forcing tx of solitary ack for duplicate MessageCounter:", tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # IN Interaction
    elif re.search(re.escape("IN"), tab[3]):
        if re.search(r"^SecureSession", tab[4]):
            pass 
        elif re.search(r"^New secure session activated for device", tab[4]):
            pass
        elif re.search(r"^Received a duplicate message with MessageCounter:", tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # SC Security
    elif re.search(re.escape("SC"), tab[3]):
        if re.search(r"Sigma[123]", tab[4]):
            pass
        elif re.search(r"^Peer assigned session session ID", tab[4]):
            pass
        elif re.search(r"^Found MRP parameters in the message", tab[4]):
            pass
        elif re.search(r"^Success status report received. Session was established", tab[4]):
            pass
        elif re.search(r"^SecureSession\[", tab[4]):
            pass
        elif re.search(r"^Initiating session on local FabricIndex", tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # ZCL ZAP Tool Config
    elif re.search(re.escape("ZCL"), tab[3]):
        if re.search(r"^Using ZAP configuration...", tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # CTL Control
    elif re.search(re.escape("CTL"), tab[3]):
        if re.search(r"^System State Initialized...", tab[4]):
            pass
        elif re.search(r"^Creating New Device Controller", tab[4]):
            pass
        elif re.search(r"^Setting CSR nonce to random value", tab[4]):
            pass
        elif re.search(r"^Setting attestation nonce to random value", tab[4]):
            pass
        elif re.search(r"^Generating NOC", tab[4]):
            pass
        elif re.search(r"^Joined the fabric at index", tab[4]):
            pass
        elif re.search(r"^\*\*\* Missing DeviceAttestationVerifier configuration", tab[4]):
            pass
        elif re.search(r"^Key Not Found", tab[4]):
            skip = True
        elif re.search(r"^StorageAdapter::", tab[4]):
            skip = True
        elif re.search(r"^Key Found", tab[4]):
            skip = True
        elif re.search(r"^Buf not big enough", tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # DL Data Layer 
    elif re.search(re.escape("DL"), tab[3]):
        if re.search(r"^CHIP task running", tab[4]):
            pass
        elif re.search(r"^HandlePlatformSpecificBLEEvent", tab[4]):
            pass
        elif re.search(r"^Long dispatch time:", tab[4]):
            pass
        elif re.search(r"^No wifi interface name. Ignoring IP update event.", tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # SPT Support
    elif re.search(re.escape("SPT"), tab[3]):
        if re.search(r"^Using device attestation PAA trust store path", tab[4]):
            pass
        elif re.search(r"^Setting up group data for Fabric Index 1 with Compressed Fabric ID:", tab[4]):
            Msg.new(tab, "resume.csv")
            skip = True
        elif re.search(r"^0x", tab[4]):
            Msg.add(tab[4])
            Msg.close()
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # FP Fabric Provisioning
    elif re.search(re.escape("FP"), tab[3]):
        if re.search(r"^Validating NOC chain", tab[4]):
            pass
        elif re.search(r"^NOC chain validation successful", tab[4]):
            pass
        elif re.search(r"^Updated fabric at index:", tab[4]):
            pass
        elif re.search(r"^Metadata for Fabric", tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # TS Time
    elif re.search(re.escape("TS"), tab[3]):
        if re.search(r"^Last Known Good Time:", tab[4]):
            skip = True
        elif re.search(r"^New proposed Last Known Good Time:", tab[4]):
            skip = True
        elif re.search(r"^Retaining current Last Known Good Time", tab[4]):
            skip = True
        elif re.search(r"^Committing Last Known Good Time to storage:", tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # CSM Commissioning
    elif re.search(re.escape("CSM"), tab[3]):
        if re.search(r"^FindOrEstablishSession:", tab[4]):
            skip = True
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # DIS Discovery
    elif re.search(re.escape("DIS"), tab[3]):
        if re.search(r"^OperationalSessionSetup", tab[4]):
            pass
        elif re.search(r"^UDP:", tab[4]):
            pass
        elif re.search(r"^Lookup clearing interface", tab[4]):
            pass
        elif re.search(r"^Checking node lookup status", tab[4]):
            pass
        elif re.search(r"^Keeping DNSSD lookup active", tab[4]):
            pass
        elif re.search(r"^Found an existing secure session to", tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    # IM Interaction Model
    elif re.search(re.escape("IM"), tab[3]):
        if re.search(r"^Received report with invalid subscriptionId", tab[4]):
            pass
        else :
            tab[4] = tab[4] + NP
        TabInFile(prefix+"resume.csv", tab, Skip=skip)

    else :
        with open(prefix+"parsing/chip.txt", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
