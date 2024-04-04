import matplotlib.pyplot as plt
from datetime import datetime


donnees = {'2024-03-01': 10, '2024-03-02': 15, '2024-03-03': 20, '2024-03-04': 25, '2024-03-05': 30}


dates = [datetime.strptime(date, '%Y-%m-%d') for date in donnees.keys()]
valeurs = list(donnees.values())


date_limite = datetime.strptime('2024-03-03', '%Y-%m-%d')


indice_date_limite = dates.index(date_limite)
plt.fill_between(dates[indice_date_limite:], [20]*len(dates[indice_date_limite:]), color='green', alpha=0.3)


plt.xlabel('Date')
plt.ylabel('Valeurs')
plt.title('Graphe avec coloration en vert à partir de la date limite')


plt.savefig("test3")
