import requests
import os
from dotenv import load_dotenv

# ==========================
# CARGA VARIABLES .env
# ==========================
load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# ==========================
# COMPETICIONES SOPORTADAS
# ==========================
# OJO: football-data.org NO tiene liga Colombiana.
SUPPORTED_COMPETITIONS = {
    "Premier League": "2021",
    "LaLiga": "2014",
    "Serie A": "2019",
    "Bundesliga": "2002",
    "Ligue 1": "2015",
    "Champions League": "2001",
}


def safe_request(url: str):
    """Hace una request segura y devuelve (json, error_msg)."""
    if not API_KEY:
        return None, "❌ FOOTBALL_API_KEY no configurada en .env"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
    except Exception as e:
        return None, f"❌ Error al conectar a la API: {e}"

    if resp.status_code != 200:
        return None, f"❌ Error API {resp.status_code}: {resp.text}"

    return resp.json(), None


def get_teams_by_league(competition_id: str):
    url = f"{BASE_URL}/competitions/{competition_id}/teams"
    data, error = safe_request(url)
    if error:
        return {"error": error}
    return data.get("teams", [])


def search_team_by_name(name: str, competition_id: str = "2021"):
    teams = get_teams_by_league(competition_id)

    if isinstance(teams, dict) and "error" in teams:
        return teams  # devolvemos el error

    for t in teams:
        if name.lower() in t["name"].lower():
            return t

    return None


def get_recent_matches_by_team(team_id: int, limit: int = 5):
    url = f"{BASE_URL}/teams/{team_id}/matches?status=FINISHED&limit={limit}"
    data, error = safe_request(url)
    if error:
        return {"error": error}
    return data.get("matches", [])


if __name__ == "__main__":
    print("API_KEY:", "OK" if API_KEY else "NO CONFIGURADA")
    team = search_team_by_name("Liverpool", competition_id="2021")
    print("Equipo encontrado:", team)

