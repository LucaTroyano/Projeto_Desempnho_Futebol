/* As tabelas aqui "criadas" são apenas uma view, faça a análise nesse mesmo arquivo. */

WITH tb_calendario AS (
    SELECT
        teamId,
        teamName as nomeTime,
        Mando,
        CASE
            WHEN Mando = "Casa" THEN 
                CASE 
                    WHEN "score.winner" = "AWAY_TEAM" THEN "Derrota"
                    WHEN "score.winner" = "HOME_TEAM" THEN "Vitória"
                    ELSE "Empate"
                END
            WHEN Mando = "Fora" THEN
                CASE
                    WHEN "score.winner" = "AWAY_TEAM" THEN "Vitória"
                    WHEN "score.winner" = "HOME_TEAM" THEN "Derrota"
                    ELSE "Empate"
                END
        END as Resultado,
        datetime(substr(DataJogo, 1,16)) as dtJogo,
        COALESCE(ROUND(tempoDescanso,2), "-") AS tempoDescanso,
        fadiga,
        codigoLiga
    FROM dados_football
    WHERE status = "FINISHED" OR status = "TIMED"
    GROUP BY nomeTime, dtJogo 
),

tb_partidas AS (
    SELECT
        id,
        teamId,
        "competition.id" as idCompeticao,
        codigoLiga,
        teamName as nomeTime,
        golsCasa,
        golsFora,
        Mando,
        datetime(substr(DataJogo, 1,16)) as dtJogo,
        status
    FROM dados_football
    ORDER BY dtJogo
)
SELECT * FROM tb_calendario;
