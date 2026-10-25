import pandas as pd
import pyodbc
from datetime import datetime

conn_str = (
    "Driver={SQL Server};"
    "Server=.;"
    "Database=LoLWorldsAnalyzer;"
    "Trusted_Connection=yes;"
)

def inyectar_datos_diarios():
    print(f"[{datetime.now()}] Iniciando Robot Nocturno de Análisis...")
    conexion = pyodbc.connect(conn_str)
    cursor_db = conexion.cursor()

    df = pd.read_csv('datos_torneos.csv', low_memory=False)
    
    # TRUCO DE DATOS: Asignamos el Primer Dragón y Barón del equipo a sus jugadores
    df['firstdragon'] = df.groupby(['gameid', 'teamname'])['firstdragon'].transform('max').fillna(0)
    df['firstbaron'] = df.groupby(['gameid', 'teamname'])['firstbaron'].transform('max').fillna(0)
    
    jugadores = df[df['position'] != 'team'].fillna(0) 
    # Filtro Mundial: Extraemos solo las partidas oficiales de Worlds sin importar el parche
    datos_meta = jugadores[jugadores['league'] == 'WLDs']
    
    contador = 0
    for index, row in datos_meta.iterrows():
        match_id = str(row['gameid'])
        player_id = str(row['playerid'])
        
        # Verificamos si la partida ya existe (Así el robot no duplica datos si corre cada día)
        cursor_db.execute("SELECT 1 FROM Partidas WHERE MatchID = ? AND PUUID = ?", (match_id, player_id))
        if not cursor_db.fetchone():
            cursor_db.execute("""
                IF NOT EXISTS (SELECT 1 FROM Jugadores WHERE PUUID = ?)
                BEGIN INSERT INTO Jugadores (PUUID, GameName, TagLine) VALUES (?, ?, 'PRO') END
            """, (player_id, player_id, str(row['playername'])))
            
            cursor_db.execute("""
                INSERT INTO Partidas (MatchID, PUUID, Campeon, Kills, Deaths, Assists, OroGanado, DanioCampeones, WardsColocados, Victoria, Parche, Liga, PrimerDragon, PrimerBaron)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (match_id, player_id, str(row['champion']), int(row['kills']), int(row['deaths']), 
                  int(row['assists']), int(row['earnedgold']), int(row['damagetochampions']), 
                  int(row['wardsplaced']), 1 if row['result'] == 1 else 0, str(row['patch']), 
                  str(row['league']), int(row['firstdragon']), int(row['firstbaron'])))
            contador += 1
            if contador % 1000 == 0: conexion.commit()

    conexion.commit()
    conexion.close()
    print(f"[{datetime.now()}] Proceso finalizado. {contador} nuevas partidas inyectadas.")

if __name__ == "__main__":
    inyectar_datos_diarios()