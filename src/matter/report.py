import filter
import pandas as pd 
import os

def nodeSubscription(succeeded, failed, connexions, output):
    tab = []
    for i in range(10):
        tab.append(["node "+str(i), 0, 0, 0, 0])
    df = pd.read_csv("csv/"+succeeded)
    for index, row in df.iterrows():
        if row[4][-2] in '0123456789':
            tab[int(row[4][-2])][1] += 1

    df = pd.read_csv("csv/"+failed)
    for index, row in df.iterrows():
        if row[4][-2] in '0123456789':
            tab[int(row[4][-2])][2] += 1
    df = pd.read_csv("csv/"+connexions)
    for index, row in df.iterrows():
        if "Matter commissioning of Node ID" in row[5]:
            n = int(row[5].split(' ')[-2])
            tab[n][3] += 1
        elif "Failed to perform commissioning step 18" in row[5]:
            n = int(df.iloc[index-1, 5].split(' ')[-3])
            tab[n][4] += 1
    node = pd.DataFrame(tab, columns=['node', 'succeeded', 'failed', 'commissinoning OK', 'commissioning failed'])
    if os.path.exists("csv/"+output):
        n = pd.read_csv("csv/"+output)
        if (not node.equals(n)):
            for index in (filter.FindDifferences(node, n)):
                if index[1] == 1 : message = "connexion succeeded"
                elif index[1] == 2 : message = "connexion failed"
                elif index[1] == 3 : message = "First connexion succeed, new device !"
                elif index[1] == 4 : message = "First connexion failed, new device not connected"
                else : message = "something unknown happend"
                print("node "+str(index[0])+ " : "+message)
            node.to_csv("csv/"+output, index=False)
    else :
        print("creating new file csv/node.csv")
        node.to_csv("csv/"+output, index=False)




