import re
import csv
import os


def parse(tab):
    if re.search(re.escape("DMG"), tab[4]):
        pass
    elif re.search(re.escape("EM"), tab[4]):
        pass
    elif re.search(re.escape("IN"), tab[4]):
        pass
    elif re.search(re.escape("SC"), tab[4]):
        pass
    elif re.search(re.escape("ZCL"), tab[4]):
        pass
    elif re.search(re.escape("CTL"), tab[4]):
        pass
    elif re.search(re.escape("DL"), tab[4]):
        pass
    elif re.search(re.escape("SPT"), tab[4]):
        pass
    elif re.search(re.escape("FP"), tab[4]):
        pass
    elif re.search(re.escape("TS"), tab[4]):
        pass
    elif re.search(re.escape("CSM"), tab[4]):
        pass
    elif re.search(re.escape("DIS"), tab[4]):
        pass
    elif re.search(re.escape("IM"), tab[4]):
        pass
    else :
        with open("parsing/chip.txt", "a") as f:
            writer = csv.writer(f)
            writer.writerow(tab)
