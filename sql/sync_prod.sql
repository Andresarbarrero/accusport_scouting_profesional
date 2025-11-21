-- ACCUST SCOUT - SYNC TO PROD
-- Aquí van SOLO cambios reales, no datos de pruebas.
-- SE EJECUTA DESDE PYTHON, NO A MANO.

-------------------------------------------------------------
-- EJEMPLOS DE ESTRUCTURA QUE PUEDES AGREGAR EN EL FUTURO
-------------------------------------------------------------

-- ALTER TABLE players ADD COLUMN IF NOT EXISTS second_position VARCHAR(50);
-- ALTER TABLE stats ADD COLUMN IF NOT EXISTS xG NUMERIC(5,2);

-------------------------------------------------------------
-- EJEMPLOS DE DATOS REALES QUE PUEDES MOVER A PRODUCCIÓN
-------------------------------------------------------------

-- INSERT INTO scouting_reports (player_id, report_date, scout_name, overall_rating, strengths, weaknesses, recommended_role, notes)
-- SELECT player_id, report_date, scout_name, overall_rating, strengths, weaknesses, recommended_role, notes
-- FROM accust_scout.scouting_reports
-- WHERE report_id = XXXX;

-- Agregar columna de valor de mercado
ALTER TABLE players ADD COLUMN IF NOT EXISTS market_value NUMERIC(12,2);

-- VIEW COMPLETA DE SCOUTING
CREATE OR REPLACE VIEW vw_player_scouting_full AS
SELECT
    p.player_id,
    p.full_name,
    p.position,
    p.nationality,
    DATE_PART('year', AGE(p.birth_date)) AS age,
    COALESCE(ROUND(AVG(sr.overall_rating), 2), 0) AS scout_rating,
    SUM(s.minutes_played) AS mins_jugados,
    SUM(s.goals) AS goles,
    SUM(s.assists) AS asistencias,
    ROUND(
        CASE WHEN SUM(s.minutes_played) > 0
             THEN (SUM(s.goals) * 90.0 / SUM(s.minutes_played))
             ELSE 0 END
    , 2) AS goles_x_90,
    ROUND(
        CASE WHEN SUM(s.assists) > 0
             THEN (SUM(s.assists) * 90.0 / SUM(s.minutes_played))
             ELSE 0 END
    , 2) AS asistencias_x_90,
    STRING_AGG(sr.strengths, '; ') AS fortalezas_resumidas,
    STRING_AGG(sr.weaknesses, '; ') AS debilidades_resumidas,
    CASE
        WHEN COALESCE(ROUND(AVG(sr.overall_rating), 2), 0) >= 8.0
             AND (SUM(s.goals) * 90.0 / NULLIF(SUM(s.minutes_played),0)) >= 0.5
        THEN 'Jugador con impacto inmediato.'
        WHEN COALESCE(ROUND(AVG(sr.overall_rating), 2), 0) >= 7.0
             AND (SUM(s.goals) * 90.0 / NULLIF(SUM(s.minutes_played),0)) >= 0.3
        THEN 'Jugador con buen rendimiento y proyección.'
        ELSE 'Perfil que requiere seguimiento.'
    END AS conclusion_profesional
FROM players p
LEFT JOIN scouting_reports sr ON sr.player_id = p.player_id
LEFT JOIN stats s ON s.player_id = p.player_id
GROUP BY p.player_id;

-- Enviar el jugador Luis Díaz a producción
INSERT INTO players (player_id, full_name, birth_date, nationality, height_cm, weight_kg, position, preferred_foot)
SELECT player_id, full_name, birth_date, nationality, height_cm, weight_kg, position, preferred_foot
WHERE full_name = 'Luis Fernando Díaz'
ON CONFLICT (player_id) DO NOTHING;

-- Enviar su scouting report
INSERT INTO scouting_reports (player_id, report_date, scout_name, overall_rating, strengths, weaknesses, recommended_role, notes)
SELECT player_id, report_date, scout_name, overall_rating, strengths, weaknesses, recommended_role, notes
WHERE player_id = (SELECT player_id FROM accust_scout WHERE full_name = 'Luis Fernando Díaz')
ON CONFLICT DO NOTHING;

-- Enviar sus estadísticas
INSERT INTO stats (match_id, player_id, minutes_played, goals, assists, shots, passes, tackles, yellow_cards, red_cards)
SELECT match_id, player_id, minutes_played, goals, assists, shots, passes, tackles, yellow_cards, red_cards
WHERE player_id = (SELECT player_id FROM accust_scout.public.players WHERE full_name = 'Luis Fernando Díaz')
ON CONFLICT DO NOTHING;

