# ETL FOOTBALL

Projeto de ETL feito em Python utilizando a API football-data.org.

Esse projeto visa a visão de analisar desempenho físico no esporte. 

## Tecnologias utilizadas

- Python: Bibliotecas - Pandas, SQLAlchemy, JSON e Requests.
- SQLITE3.

## Como usar

Primeiro, você deve instalar as bibliotecas na sua máquina caso essas não estejam instaladas:

```
pip install pandas
```
```
pip install sqlalchemy
```

#### Ao executar o programa, esse criará:

- 3 arquivos JSON referentes aos dados de partidas das competições: Premier League, La Liga e Champions League.
- Um arquivo .db onde os dados tratados foram exportados.

Execute o Script em SQLITE3.

## Como os dados foram tratados

Os dados extraídos da API são referente a partidas das competições: Premier League, La Liga e Champions League. Ou seja, informações sobre elenco e informações específicas por jogador não estão inclusas nesse proejto.

Os dados foram tratados de maneira a elucidar uma visão de desempenho físico, assim sendo, **foi calculado quanto tempo de descanso cada time teve após a partida anterior** e com base nisso, sumarizado em:

- Pouca Fadiga, para tempo de descanso maior ou igual que 5 dias.
- Fadiga Risco, para tempo de descanso entre 3 e 4 dias.
- Fadiga Crítica para tempo de descanso menor ou igual a 3 dias.

Assim, é possível analisar cada time na base de dados com SQL.

