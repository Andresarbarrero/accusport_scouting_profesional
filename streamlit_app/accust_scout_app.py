import streamlit as st
import psycopg2
from psycopg2.extras import DictCursor
from datetime import date

from external_api import SUPPORTED_COMPETITIONS
from reporting_api import generar_reporte_con_partido_real

# ===========================
# CONFIGURACIÓN BD DESDE SECRETS (STREAMLIT CLOUD)
# ===========================
DB_CONFIG = {
    "host": st.secrets["DB_HOST"],
    "port": int(st.secrets["DB_PORT"]),
    "dbname": st.secrets["DB_NAME"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
}

# ===========================
# HELPERS DE CONEXIÓN
# ===========================
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_all(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
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


# ===========================
# LÓGICA DE JUGADORES
# ===========================
def get_players():
    rows = fetch_all(
        """
        SELECT
            player_id,
            full_name,
            birth_date,
            nationality,
            position,
            height_cm,
            weight_kg
        FROM players
        ORDER BY full_name
        """
    )
    return rows


def find_player_by_identity(full_name, birth_date, nationality):
    rows = fetch_all(
        """
        SELECT player_id, full_name, birth_date, nationality, position
        FROM players
        WHERE LOWER(full_name) = LOWER(%s)
          AND birth_date = %s
          AND LOWER(COALESCE(nationality, '')) = LOWER(COALESCE(%s, ''))
        """,
        (full_name, birth_date, nationality),
    )
    if rows:
        return rows[0]
    return None


def insert_player(
    full_name, birth_date, nationality, height_cm, weight_kg, position, preferred_foot
):
    try:
        execute_query(
            """
            INSERT INTO players (
                full_name, birth_date, nationality,
                height_cm, weight_kg, position, preferred_foot
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                full_name,
                birth_date,
                nationality if nationality else None,
                height_cm if height_cm else None,
                weight_kg if weight_kg else None,
                position if position else None,
                preferred_foot if preferred_foot else None,
            ),
        )
        return True, None
    except Exception as e:
        if "uq_players_identity" in str(e):
            return (
                False,
                "Ya existe un jugador con ese nombre, fecha de nacimiento y nacionalidad.",
            )
        return False, str(e)


def update_player(player_id, nationality, height_cm, weight_kg, position, preferred_foot):
    try:
        execute_query(
            """
            UPDATE players
            SET nationality = %s,
                height_cm = %s,
                weight_kg = %s,
                position = %s,
                preferred_foot = %s
            WHERE player_id = %s
            """,
            (
                nationality if nationality else None,
                height_cm if height_cm else None,
                weight_kg if weight_kg else None,
                position if position else None,
                preferred_foot if preferred_foot else None,
                player_id,
            ),
        )
        return True, None
    except Exception as e:
        return False, str(e)


# ===========================
# LÓGICA LIGAS / EQUIPOS / PARTIDOS
# ===========================
def get_or_create_league(name, country, level=None):
    row = fetch_all(
        "SELECT league_id FROM leagues WHERE name = %s AND country = %s",
        (name, country),
    )
    if row:
        return row[0]["league_id"]

    execute_query(
        "INSERT INTO leagues (name, country, level) VALUES (%s,%s,%s)",
        (name, country, level),
    )
    row = fetch_all(
        "SELECT league_id FROM leagues WHERE name = %s AND country = %s",
        (name, country),
    )
    return row[0]["league_id"]


def get_or_create_team(name, league_id):
    row = fetch_all(
        "SELECT team_id FROM teams WHERE name = %s AND league_id = %s",
        (name, league_id),
    )
    if row:
        return row[0]["team_id"]

    execute_query(
        "INSERT INTO teams (name, league_id) VALUES (%s,%s)",
        (name, league_id),
    )
    row = fetch_all(
        "SELECT team_id FROM teams WHERE name = %s AND league_id = %s",
        (name, league_id),
    )
    return row[0]["team_id"]


def create_match(match_date, league_id, home_team_id, away_team_id, venue=None):
    execute_query(
        """
        INSERT INTO matches (match_date, home_team_id, away_team_id, league_id, venue)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (match_date, home_team_id, away_team_id, league_id, venue),
    )
    row = fetch_all(
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
    return row[0]["match_id"]


# ===========================
# STATS / REPORTES
# ===========================
def insert_stats(
    match_id,
    player_id,
    minutes_played,
    goals,
    assists,
    shots,
    passes,
    tackles,
    yellow_cards,
    red_cards,
):
    execute_query(
        """
        INSERT INTO stats (
            match_id, player_id, minutes_played,
            goals, assists, shots, passes, tackles,
            yellow_cards, red_cards
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            match_id,
            player_id,
            minutes_played,
            goals,
            assists,
            shots,
            passes,
            tackles,
            yellow_cards,
            red_cards,
        ),
    )


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


# ===========================
# UI STREAMLIT
# ===========================
st.set_page_config(
    page_title="AccustScout - Plataforma interna",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ AccustScout - Plataforma interna de Scouting")

with st.expander("📘 Guía rápida para llenar el formulario (recomendado)"):
    st.markdown(
        """
        Aquí puedes explicar a otros scouts cómo usar la plataforma.
        (Este texto ya lo tenías, si quieres luego lo volvemos a poner completo.)
        """
    )

st.sidebar.title("Navegación")
section = st.sidebar.radio(
    "Secciones",
    [
        "➕ Registrar nuevo jugador",
        "👤 Gestionar jugador existente",
        "🔍 Scouting asistido por API",
    ],
)

# ==================================
# SECCIÓN 1: NUEVO JUGADOR
# ==================================
if section == "➕ Registrar nuevo jugador":
    st.subheader("Registro de nuevo jugador")

    with st.form("new_player_form"):
        full_name = st.text_input("Nombre completo *")
        col1, col2 = st.columns(2)
        with col1:
            birth_date = st.date_input(
                "Fecha de nacimiento *",
                value=date(2005, 1, 1),
                min_value=date(1970, 1, 1),
                max_value=date(2025, 12, 31),
            )
        with col2:
            nationality = st.text_input("Nacionalidad", value="Colombia")

        col3, col4 = st.columns(2)
        with col3:
            height_cm = st.number_input(
                "Altura (cm)", min_value=120, max_value=220, step=1, value=175
            )
        with col4:
            weight_kg = st.number_input(
                "Peso (kg)", min_value=40, max_value=120, step=1, value=70
            )

        position = st.text_input(
            "Posición (ej: Extremo, Delantero, Volante, Central) *"
        )
        preferred_foot = st.selectbox(
            "Pie dominante", ["Derecho", "Izquierdo", "Ambidiestro"]
        )

        submitted = st.form_submit_button("💾 Guardar jugador")

        if submitted:
            if not full_name.strip():
                st.error("El campo **Nombre completo** es obligatorio.")
            elif not position.strip():
                st.error("El campo **Posición** es obligatorio.")
            elif not nationality.strip():
                st.error("El campo **Nacionalidad** es obligatorio.")
            else:
                existing = find_player_by_identity(
                    full_name=full_name.strip(),
                    birth_date=birth_date,
                    nationality=nationality.strip(),
                )
                if existing:
                    st.warning(
                        f"⚠ Ya existe un jugador con estos datos: "
                        f"**{existing['full_name']} ({existing['nationality']}, {existing['birth_date']})**.\n\n"
                        f"Ve a la sección **'Gestionar jugador existente'** para actualizarlo o añadirle un reporte."
                    )
                else:
                    ok, error_msg = insert_player(
                        full_name=full_name.strip(),
                        birth_date=birth_date,
                        nationality=nationality.strip() if nationality else None,
                        height_cm=int(height_cm) if height_cm else None,
                        weight_kg=int(weight_kg) if weight_kg else None,
                        position=position.strip(),
                        preferred_foot=preferred_foot,
                    )
                    if ok:
                        st.success(f"✅ Jugador **{full_name}** añadido correctamente.")
                    else:
                        st.error("❌ No se pudo guardar el jugador.")
                        st.code(error_msg, language="text")


# ==================================
# SECCIÓN 2: GESTIONAR JUGADOR
# ==================================
elif section == "👤 Gestionar jugador existente":
    st.subheader("Gestión de jugador existente")

    players = get_players()
    if not players:
        st.info("No hay jugadores registrados todavía.")
    else:
        player_options = {
            f"{p['full_name']} ({p['nationality']}, {p['birth_date']})": p["player_id"]
            for p in players
        }
        selected_label = st.selectbox(
            "Selecciona un jugador", list(player_options.keys())
        )
        selected_player_id = player_options[selected_label]

        player_row = [p for p in players if p["player_id"] == selected_player_id][0]

        st.markdown(f"### 🧾 Ficha básica: {player_row['full_name']}")

        col_a, col_b = st.columns(2)

        # -------- Actualizar datos básicos --------
        with col_a:
            st.markdown("#### ✏️ Actualizar datos básicos")
            up_nat = st.text_input(
                "Nacionalidad", value=player_row["nationality"] or ""
            )
            up_pos = st.text_input("Posición", value=player_row["position"] or "")
            up_height = st.number_input(
                "Altura (cm)",
                min_value=120,
                max_value=220,
                value=player_row["height_cm"]
                if player_row["height_cm"] is not None
                else 175,
            )
            up_weight = st.number_input(
                "Peso (kg)",
                min_value=40,
                max_value=120,
                value=player_row["weight_kg"]
                if player_row["weight_kg"] is not None
                else 70,
            )
            up_foot = st.selectbox(
                "Pie dominante", ["Derecho", "Izquierdo", "Ambidiestro"]
            )

            if st.button("💾 Guardar cambios de jugador"):
                ok, err = update_player(
                    player_id=selected_player_id,
                    nationality=up_nat.strip() if up_nat else None,
                    height_cm=int(up_height),
                    weight_kg=int(up_weight),
                    position=up_pos.strip() if up_pos else None,
                    preferred_foot=up_foot,
                )
                if ok:
                    st.success("Datos del jugador actualizados correctamente.")
                else:
                    st.error("Error al actualizar jugador.")
                    st.code(err, language="text")

        # -------- Añadir STATS de partido --------
        with col_b:
            st.markdown("#### 📊 Añadir estadísticas de partido")

            with st.form("stats_form"):
                match_date = st.date_input("Fecha del partido", value=date.today())
                league_name = st.text_input("Liga (nombre)", value="Liga Colombiana A")
                league_country = st.text_input("País de la liga", value="Colombia")
                venue = st.text_input("Estadio / sede", value="")

                home_team = st.text_input("Equipo local", value="Equipo Local")
                away_team = st.text_input("Equipo visitante", value="Equipo Visitante")

                st.write("Estadísticas del jugador en este partido:")

                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    minutes_played = st.number_input(
                        "Minutos jugados", min_value=0, max_value=120, value=90
                    )
                    goals = st.number_input("Goles", 0, 10, 0)
                    assists = st.number_input("Asistencias", 0, 10, 0)
                with col_s2:
                    shots = st.number_input("Tiros", 0, 20, 0)
                    passes = st.number_input("Pases", 0, 200, 0)
                    tackles = st.number_input("Entradas", 0, 20, 0)
                with col_s3:
                    yellow_cards = st.number_input("Amarillas", 0, 2, 0)
                    red_cards = st.number_input("Rojas", 0, 1, 0)

                    submitted_stats = st.form_submit_button(
                        "➕ Registrar estadísticas de este partido"
                    )

            if submitted_stats:
                if minutes_played <= 0:
                    st.error("Los **minutos jugados** deben ser mayores a 0.")
                elif minutes_played > 120:
                    st.error(
                        "Los **minutos jugados** no pueden ser mayores a 120."
                    )
                else:
                    league_id = get_or_create_league(
                        league_name.strip(), league_country.strip()
                    )
                    home_team_id = get_or_create_team(home_team.strip(), league_id)
                    away_team_id = get_or_create_team(away_team.strip(), league_id)
                    match_id = create_match(
                        match_date=match_date,
                        league_id=league_id,
                        home_team_id=home_team_id,
                        away_team_id=away_team_id,
                        venue=venue.strip() if venue else None,
                    )
                    insert_stats(
                        match_id=match_id,
                        player_id=selected_player_id,
                        minutes_played=int(minutes_played),
                        goals=int(goals),
                        assists=int(assists),
                        shots=int(shots),
                        passes=int(passes),
                        tackles=int(tackles),
                        yellow_cards=int(yellow_cards),
                        red_cards=int(red_cards),
                    )
                    st.success("📊 Estadísticas del partido registradas correctamente.")

        st.markdown("---")
        st.markdown("#### 📝 Añadir reporte de scouting")

        with st.form("scouting_form"):
            report_date = st.date_input("Fecha del reporte", value=date.today())
            scout_name = st.text_input("Nombre del scout", value="Andrés Barrero")
            overall_rating = st.slider(
                "Valoración global (0.0 a 10.0)", 0.0, 10.0, 7.5, 0.1
            )

            strengths = st.text_area(
                "Fortalezas (separadas por frases)",
                value="Buena aceleración, regate y desborde.",
            )
            weaknesses = st.text_area(
                "Debilidades",
                value="Decisiones mejorables en último tercio.",
            )
            recommended_role = st.text_input(
                "Rol recomendado", value="Extremo de transición ofensiva"
            )
            notes = st.text_area(
                "Notas adicionales",
                value="Jugador con potencial para ligas de mayor ritmo.",
            )

            submitted_report = st.form_submit_button(
                "➕ Guardar reporte de scouting"
            )

        if submitted_report:
            if not strengths.strip():
                st.error("Debes ingresar al menos **una fortaleza**.")
            elif not weaknesses.strip():
                st.error("Debes ingresar al menos **una debilidad**.")
            elif overall_rating < 0 or overall_rating > 10:
                st.error("La valoración global debe estar entre **0.0 y 10.0**.")
            else:
                insert_scouting_report(
                    player_id=selected_player_id,
                    report_date=report_date,
                    scout_name=scout_name.strip() if scout_name else None,
                    overall_rating=float(overall_rating),
                    strengths=strengths.strip() if strengths else None,
                    weaknesses=weaknesses.strip() if weaknesses else None,
                    recommended_role=recommended_role.strip()
                    if recommended_role
                    else None,
                    notes=notes.strip() if notes else None,
                )
                st.success("📝 Reporte de scouting guardado correctamente.")


# ==================================
# SECCIÓN 3: SCOUTING ASISTIDO POR API
# ==================================
elif section == "🔍 Scouting asistido por API":
    st.subheader("Scouting asistido con contexto real (football-data.org)")

    players = get_players()
    if not players:
        st.info("No hay jugadores registrados todavía.")
    else:
        player_options = {
            f"{p['full_name']} ({p['nationality']}, {p['birth_date']})": p["player_id"]
            for p in players
        }
        selected_label = st.selectbox(
            "Selecciona un jugador observado", list(player_options.keys())
        )
        selected_player_id = player_options[selected_label]

        competition_name = st.selectbox(
            "Competición (API)",
            list(SUPPORTED_COMPETITIONS.keys()),
        )
        competition_id = SUPPORTED_COMPETITIONS[competition_name]

        team_name = st.text_input(
            "Nombre del equipo real (ej: Liverpool, PSG, Bayern)",
            value="Liverpool",
        )

        if st.button("➕ Generar reporte con contexto real"):
            ok, msg = generar_reporte_con_partido_real(
                player_id=selected_player_id,
                team_name=team_name.strip(),
                competition_id=competition_id,
            )
            if ok:
                st.success("📝 Reporte de scouting generado correctamente.")
                if msg:
                    st.info(msg)
            else:
                st.error("❌ No se pudo generar el reporte.")
                if msg:
                    st.code(msg, language="text")
