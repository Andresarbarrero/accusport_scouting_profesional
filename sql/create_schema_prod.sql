-- ACCUST SCOUT – ESQUEMA PRODUCCIÓN
-- NO borrar ni reiniciar este esquema

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- LIGAS
CREATE TABLE IF NOT EXISTS leagues (
    league_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    level INT,
    created_at TIMESTAMP DEFAULT now()
);

-- EQUIPOS
CREATE TABLE IF NOT EXISTS teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    league_id INT REFERENCES leagues(league_id),
    founded_year INT,
    stadium VARCHAR(200),
    created_at TIMESTAMP DEFAULT now()
);

-- JUGADORES
CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    birth_date DATE NOT NULL,
    nationality VARCHAR(80),
    height_cm INT,
    weight_kg INT,
    position VARCHAR(50),
    preferred_foot VARCHAR(20),
    created_at TIMESTAMP DEFAULT now()
);

-- PARTIDOS
CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    home_team_id INT REFERENCES teams(team_id),
    away_team_id INT REFERENCES teams(team_id),
    league_id INT REFERENCES leagues(league_id),
    venue VARCHAR(150),
    created_at TIMESTAMP DEFAULT now()
);

-- ESTADISTICAS
CREATE TABLE IF NOT EXISTS stats (
    stat_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    player_id INT REFERENCES players(player_id),
    minutes_played INT,
    goals INT,
    assists INT,
    shots INT,
    passes INT,
    tackles INT,
    yellow_cards INT,
    red_cards INT
);

-- REPORTES DE SCOUTING
CREATE TABLE IF NOT EXISTS scouting_reports (
    report_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    report_date DATE NOT NULL,
    scout_name VARCHAR(100),
    overall_rating NUMERIC(3,1),
    strengths TEXT,
    weaknesses TEXT,
    recommended_role VARCHAR(150),
    notes TEXT
);
