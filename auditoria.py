import pandas as pd

df = pd.read_csv('datos_torneos.csv', low_memory=False)
equipos = df[df['position'] == 'team']
# Buscamos las últimas 5 partidas donde el nombre del equipo contenga "T1"
t1_partidas = equipos[equipos['teamname'].str.contains('T1', na=False)].tail(5)
print(t1_partidas[['date', 'teamname', 'patch', 'league']])