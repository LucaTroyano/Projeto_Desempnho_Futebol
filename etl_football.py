import pandas as pd
import sqlalchemy
import requests
import json

headers = { 'X-Auth-Token': '9644f5c476f54527b66accf972400756' } # Coloque aqui o seu token
def extracao():
    ligas = ['PL', 'CL', 'PD', 'FL1', 'SA', 'BL1', 'DED']
    dfs = []
    for i in ligas:
        uri = f"http://api.football-data.org/v4/competitions/{i}/matches?season=2025"
        try:
            response = requests.get(uri, headers=headers, timeout=10).json()
        except requests.exceptions.HTTPError as errh:
            print(f"Erro HTTP: {errh}")
        with open(f'{i}_2025', 'w') as f:
            json.dump(response,f,indent=4)
        with open(f'{i}_2025', 'r') as leitura:
            dados = json.load(leitura)
        codigo_liga = dados['competition']['code']
        df = pd.json_normalize(dados['matches'])
        df['codigoLiga'] = codigo_liga
        dfs.append(df)
    return dfs
def juncao_dataframes(dfs: list):
    inter_df = pd.concat(dfs)
    df_home = inter_df[["utcDate", "id", "competition.id", "status", "homeTeam.name", "homeTeam.id","score.fullTime.home", "score.winner", "codigoLiga"]]
    df_home["Mando"] = "Casa"
    df_home = df_home.rename(columns={"homeTeam.id" : "teamId", "homeTeam.name" : "teamName", "score.fullTime.home" : "golsCasa"})
    df_away = inter_df[["utcDate", "id", "competition.id", "status", "awayTeam.name", "awayTeam.id", "score.fullTime.away", "score.winner", "codigoLiga"]]
    df_away["Mando"] = "Fora"
    df_away = df_away.rename(columns={"awayTeam.id" : "teamId", "awayTeam.name" : "teamName", "score.fullTime.away" : "golsFora"})
    df_complete = pd.concat([df_home, df_away], ignore_index=True)
    return df_complete

def tratamento(df:pd.DataFrame):
    df["DataJogo"] = pd.to_datetime(df["utcDate"])
    df = df.drop(columns=['utcDate'], axis=1)
    df = df.sort_values(by=["teamId", "DataJogo"])
    df["tempoDescanso"] = df.groupby(by=["teamId"])["DataJogo"].diff()
    df = df.fillna("-")
    df["fadiga"] = "Crítica"
    df["tempoDescanso"] = pd.to_timedelta(df["tempoDescanso"],errors='coerce')
    df.loc[df["tempoDescanso"].dt.days >= 5, "fadiga"] = 'Pouca'
    df.loc[df["tempoDescanso"].dt.days < 5, "fadiga"] = 'Risco'
    df.loc[df["tempoDescanso"].dt.days < 3, "fadiga"] = 'Crítica'
    df["tempoDescanso"] = (df["tempoDescanso"].dt.total_seconds() / 86400)
    return df
def criar_conexao_banco(dados: pd.DataFrame):
    engine = sqlalchemy.create_engine("sqlite:///football_db.db")
    dados.to_sql("dados_football", engine)

lista = extracao()
dataframe = tratamento(juncao_dataframes(lista))
criar_conexao_banco(dataframe)



    