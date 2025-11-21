import os
from datetime import date

import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from external_api import search_team_by_name, get_recent_matches_by_team

# ==========================
# CARGA .env Y CONFIG BD
# ==========================
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_one(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchone()
    finally:
        conn.close()


def execute_query(query, params=None):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
    finally:
        conn.close()


# ==========================
# HELPERS BD (LIGA / EQUIPO / PARTIDO / REPORTE)
# ==========================
def get_or_create_league(name: str, country: str, level=None) -> int:
    row = fetch_one(
        "SELECT league_id FROM leagues WHERE name = %s AND country = %s",
        (name, country),
    )
    if row:
        return row["league_id"]

    execute_query(
        "INSERT INTO leagues (name, country, level) VALUES (%s,%s,%s)",
        (name, country, level),
    )
    row = fetch_one(
        "SELECT league_id FROM leagues WHERE name = %s AND country = %s",
        (name, country),
    )
    return row["league_id"]


def get_or_create_team(name: str, league_id: int) -> int:
    row = fetch_one(
        "SELECT team_id FROM teams WHERE name = %s AND league_id = %s",
        (name, league_id),
    )
    if row:
        return row["team_id"]

    execute_query(
        "INSERT INTO teams (name, league_id) VALUES (%s,%s)",
        (name, league_id),
    )
    row = fetch_one(
        "SELECT team_id FROM teams WHERE name = %s AND league_id = %s",
        (name, league_id),
    )
    return row["team_id"]


def create_match(match_date, league_id, home_team_id, away_team_id, venue=None) -> int:
    execute_query(
        """
        INSERT INTO matches (match_date, home_team_id, away_team_id, league_id, venue)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (match_date, home_team_id, away_team_id, league_id, venue),
    )
    row = fetch_one(
        """
        SELECT match_id
        FROM matches
        WHERE match_date = %s
          AND home_team_id = %s
          AND away_team_id = %s
          AND league_id = %s
        ORDER BY match_id DESC
        LIMIT 1
        """,
        (match_date, home_team_id, away_team_id, league_id),
    )
    return row["match_id"]


def insert_scouting_report(
    player_id,
    report_date,
    scout_name,
    overall_rating,
    strengths,
    weaknesses,
    recommended_role,
    notes,
):
    execute_query(
        """
        INSERT INTO scouting_reports (
            player_id, report_date, scout_name, overall_rating,
            strengths, weaknesses, recommended_role, notes
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            player_id,
            report_date,
            scout_name,
            overall_rating,
            strengths,
            weaknesses,
            recommended_role,
            notes,
        ),
    )


# ==========================
# FUNCIÓN PRINCIPAL USADA POR STREAMLIT
# ==========================
def generar_reporte_con_partido_real(player_id: int, team_name: str, competition_id: str):
    """
    1) Busca el equipo en la competición seleccionada.
    2) Obtiene el último partido jugado.
    3) Crea liga/equipos/partido en tu BD.
    4) Inserta un reporte de scouting 'automático'.
    """

    team = search_team_by_name(team_name, competition_id=competition_id)
    if team is None:
        return False, "No se encontró un equipo con ese nombre en la competición seleccionada."

    if isinstance(team, dict) and "error" in team:
        return False, f"Error al consultar equipo en API: {team['error']}"

    matches = get_recent_matches_by_team(team["id"], limit=5)
    if isinstance(matches, dict) and "error" in matches:
        return False, f"Error al obtener partidos del equipo: {matches['error']}"

    if not matches:
        return False, "No se encontraron partidos recientes para este equipo."

    match = matches[0]  # último partido
    home_name = match["homeTeam"]["name"]
    away_name = match["awayTeam"]["name"]
    match_date = match["utcDate"][:10]

    competition = match.get("competition", {})
    league_name = competition.get("name", "Competición desconocida")
    league_country = competition.get("area", {}).get("name", "Desconocido")

    league_id = get_or_create_league(league_name, league_country)
    home_id = get_or_create_team(home_name, league_id)
    away_id = get_or_create_team(away_name, league_id)

    _match_id = create_match(
        match_date=match_date,
        league_id=league_id,
        home_team_id=home_id,
        away_team_id=away_id,
        venue=match.get("venue", None),
    )

    insert_scouting_report(
        player_id=player_id,
        report_date=date.today(),
        scout_name="Scouting Automático API",
        overall_rating=6.5,
        strengths=f"Evaluado en contexto real ({home_name} vs {away_name}). Buen posicionamiento.",
        weaknesses="Impacto ofensivo limitado en el contexto observado.",
        recommended_role="Jugador a seguimiento según rol actual.",
        notes=f"Partido tomado desde football-data.org: {home_name} vs {away_name} ({match_date}).",
    )

    return True, f"Reporte generado usando el partido real {home_name} vs {away_name} del {match_date}"

