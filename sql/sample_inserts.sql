-- ======================================
-- ACCUST SCOUT – Sample Data (COMPLETO)
-- Incluye: leagues, teams, players,
-- matches, stats, scouting_reports
-- ======================================

-- LIGAS
INSERT INTO leagues (name, country, level) VALUES
('Liga Colombiana A', 'Colombia', 1),
('Liga Argentina Profesional', 'Argentina', 1),
('Premier League', 'Inglaterra', 1);

-- EQUIPOS
INSERT INTO teams (name, league_id, founded_year, stadium) VALUES
('Millonarios FC', 1, 1946, 'El Campín'),
('Atlético Nacional', 1, 1947, 'Atanasio Girardot'),
('River Plate', 2, 1901, 'Monumental'),
('Boca Juniors', 2, 1905, 'La Bombonera'),
('Manchester City', 3, 1880, 'Etihad Stadium'),
('Arsenal FC', 3, 1886, 'Emirates Stadium');

-- JUGADORES
INSERT INTO players (full_name, birth_date, nationality, height_cm, weight_kg, position, preferred_foot) VALUES
('Juan Ortiz', '2003-05-12', 'Colombia', 175, 70, 'Delantero', 'Derecho'),
('Carlos Pérez', '2000-11-03', 'Colombia', 182, 75, 'Defensa Central', 'Derecho'),
('Matías Núñez', '2002-08-21', 'Argentina', 178, 72, 'Volante', 'Izquierdo'),
('Tomás Herrera', '1999-02-17', 'Argentina', 185, 80, 'Arquero', 'Derecho'),
('James Holden', '2001-07-07', 'Inglaterra', 180, 73, 'Extremo', 'Derecho'),
('Oliver Kane', '2004-03-28', 'Inglaterra', 188, 82, 'Delantero', 'Izquierdo');

-- PARTIDOS
INSERT INTO matches (match_date, home_team_id, away_team_id, league_id, venue) VALUES
('2025-02-15', 1, 2, 1, 'El Campín'),
('2025-03-02', 3, 4, 2, 'Monumental'),
('2025-03-10', 5, 6, 3, 'Etihad Stadium');

-- ESTADÍSTICAS
INSERT INTO stats (match_id, player_id, minutes_played, goals, assists, shots, passes, tackles, yellow_cards, red_cards)
VALUES
(1, 1, 90, 1, 0, 3, 25, 1, 0, 0),
(1, 2, 90, 0, 0, 0, 40, 5, 1, 0),
(2, 3, 85, 0, 1, 2, 58, 3, 0, 0),
(2, 4, 90, 0, 0, 0, 30, 0, 0, 0),
(3, 5, 78, 1, 1, 4, 50, 2, 0, 0),
(3, 6, 90, 2, 0, 5, 22, 1, 0, 0);

-- SCOUTING REPORTS
INSERT INTO scouting_reports 
(player_id, report_date, scout_name, overall_rating, strengths, weaknesses, recommended_role, notes)
VALUES
(1, '2025-02-20', 'Andrés Barrero', 7.5,
 'Buena aceleración, regate y desborde en 1v1 por banda.',
 'Centros inconsistentes, decisiones irregulares en último tercio.',
 'Extremo derecho (inside winger)',
 'Jugador ideal para transiciones rápidas. Tiene potencial de crecimiento.'),

(2, '2025-02-21', 'Andrés Barrero', 7.8,
 'Solidez defensiva, buen juego aéreo, liderazgo en la línea defensiva.',
 'Lento girando, salida de balón mejorable bajo presión.',
 'Central de línea de 4',
 'Gran perfil físico, opción interesante para ligas exigentes.'),

(3, '2025-03-01', 'Andrés Barrero', 7.2,
 'Excelente visión, pase entre líneas y lectura táctica.',
 'Físico bajo, dificultades en transiciones defensivas.',
 'Interior mixto / Volante creativo',
 'Aporta claridad con balón, ideal para equipos de posesión.'),

(5, '2025-03-12', 'Andrés Barrero', 8.0,
 'Muy desequilibrante, gran cambio de ritmo y buen disparo.',
 'Defensa posicional irregular, baja intensidad sin balón.',
 'Extremo ofensivo',
 'Jugador con gran impacto ofensivo pero requiere libertad táctica.'),

(6, '2025-03-15', 'Andrés Barrero', 8.3,
 'Excelente finalización, gran lectura de movimientos en área.',
 'Poca participación en build-up, depende de recibir balones.',
 'Delantero de área',
 'Muy buen perfil para equipos que producen muchos centros.');
