import datetime
from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

def GenerateDates(dates):
    first = dates[0]
    end = dates[1]
    
    start_date = datetime.date(int(first[0]), int(first[1]), int(first[2]))
    end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))
    delta = datetime.timedelta(days=1)
    
    dates_dict = {}
    current_date = start_date - 10*delta
    while current_date <= end_date + 10*delta:
        dates_dict[current_date.strftime('%Y-%m-%d')] = 0
        current_date += delta
    return dates_dict

def GetDate(file):
    df = pd.read_csv("csv/"+file)
    shape = df.shape
    return [df.iloc[0,0].split('-'), df.iloc[shape[0]-1,0].split('-')]

def FillDict(node, succeeded, failed, connexions):
    d = [GenerateDates(GetDate("matter_logs.csv")),GenerateDates(GetDate("matter_logs.csv")),GenerateDates(GetDate("matter_logs.csv")),GenerateDates(GetDate("matter_logs.csv"))]
    df = pd.read_csv("csv/"+succeeded)
    for index, row in df.iterrows():
        if row[4][-2] in '0123456789' and int(row[4][-2]) == node:
            d[0][row[0]] += 1

    df = pd.read_csv("csv/"+failed)
    for index, row in df.iterrows():
        if row[4][-2] in '0123456789' and int(row[4][-2]) == node:
            d[1][row[0]] += 1
    df = pd.read_csv("csv/"+connexions)
    for index, row in df.iterrows():
        if "Matter commissioning of Node ID" in row[5] and int(row[5].split(' ')[-2]) == node:
            d[2][row[0]] += 1
        elif "Failed to perform commissioning step 18" in row[5] and int(df.iloc[index-1, 5].split(' ')[-3]) == node:
            d[3][row[0]] += 1
    return d

def GetPlot(data ):
    data1 = data[0]
    data2 = data[1]
    data3 = data[2]
    data4 = data[3]

    m = 0
    for i in range(4):
        if max(data[i].items(), key=lambda x: x[1])[1] > m : 
            m = max(data[i].items(), key=lambda x: x[1])[1]

    dates1, values1 = zip(*sorted(data1.items()))
    dates2, values2 = zip(*sorted(data2.items()))
    dates3, values3 = zip(*sorted(data3.items()))
    dates4, values4 = zip(*sorted(data4.items()))

    ind, val = max(data[2].items(), key=lambda x: x[1])
    dates = [dt.strptime(date, '%Y-%m-%d') for date in data[2].keys()]
    print("longueur de la data", len(data[2]))
    print("date limite", ind)
    print("longueur de dates", len(dates))
    
    date_limite = dt.strptime('2024-03-29', '%Y-%m-%d')
    
    indice_date_limite = dates.index(date_limite)
    print(dates[indice_date_limite:], [m]*len(dates[indice_date_limite:]))

    print(indice_date_limite)
    plt.fill_between(dates[indice_date_limite:], [m]*len(dates[indice_date_limite:]), color='green', alpha=0.3)


    plt.figure(figsize=(10, 6))
    plt.plot(dates1, values1, marker='o', linestyle='-', label='Data 1')
    plt.plot(dates2, values2, marker='o', linestyle='-', label='Data 2')
    plt.plot(dates3, values3, marker='o', linestyle='-', label='Data 3')
    plt.plot(dates4, values4, marker='o', linestyle='-', label='Data 4')


    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Plot with Connected Points for 4 Data Sets')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()


    plt.savefig("test")
    print("fichier ok")


GetPlot(FillDict(3, "succeeded.csv", "failed.csv", "commissioning.csv" ))

