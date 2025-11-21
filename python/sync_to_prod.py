import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()  # carga automáticamente el archivo .env

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

PROD_DB_CONFIG = {
    "host": os.getenv("PROD_DB_HOST"),
    "port": int(os.getenv("PROD_DB_PORT")),
    "dbname": os.getenv("PROD_DB_NAME"),
    "user": os.getenv("PROD_DB_USER"),
    "password": os.getenv("PROD_DB_PASSWORD"),
}

FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")


# CONFIGURACIÓN DE BASES
DEV_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "accust_scout",
    "user": "accust_scout",
    "password": "DBaccusport2025"
}

PROD_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "accust_scout_prod",
    "user": "accust_scout",
    "password": "DBaccusport2025"
}

# ORDEN CORRECTO DE TABLAS (respeta FK)
TABLES = [
    "leagues",
    "teams",
    "players",
    "matches",
    "stats",
    "scouting_reports"
]

def fetch_all_rows(conn, table):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall(), [desc[0] for desc in cur.description]

def truncate_table(conn, table):
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE")

def insert_into_table(conn, table, columns, rows):
    if not rows:
        return
    with conn.cursor() as cur:
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"
        execute_values(cur, sql, rows)

def sync_structure(dev_conn, prod_conn):
    print("🔧 Sincronizando estructura (tablas y vista)...")

    with dev_conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
        """)
        dev_tables = [t[0] for t in cur.fetchall()]

    with prod_conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
        """)
        prod_tables = [t[0] for t in cur.fetchall()]

    missing = set(dev_tables) - set(prod_tables)

    if missing:
        print("📌 Tablas faltantes en producción:", missing)

    # Crear tablas faltantes copiando el DDL desde DEV
    for table in missing:
        with dev_conn.cursor() as dev_cur, prod_conn.cursor() as prod_cur:
            dev_cur.execute(f"""
                SELECT 'CREATE TABLE ' || relname || E'\n(\n' ||
                    pg_get_tabledef(oid) || E'\n);\n'
                FROM pg_class
                WHERE relname = '{table}';
            """)
            ddl = dev_cur.fetchone()[0]
            prod_cur.execute(ddl)

    # Crear la vista (siempre se reemplaza)
    with prod_conn.cursor() as cur:
        cur.execute("DROP VIEW IF EXISTS vw_player_scouting_full")
        cur.execute("""
            CREATE VIEW vw_player_scouting_full AS
            SELECT
                p.player_id,
                p.full_name,
                p.position,
                p.nationality,
                EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.birth_date)) AS age,
                MAX(sr.overall_rating) AS scout_rating,
                SUM(s.minutes_played) AS mins_jugados,
                SUM(s.goals) AS goles,
                SUM(s.assists) AS asistencias,
                ROUND((SUM(s.goals)::numeric / NULLIF(SUM(s.minutes_played),0)) * 90, 2) AS goles_x_90,
                ROUND((SUM(s.assists)::numeric / NULLIF(SUM(s.minutes_played),0)) * 90, 2) AS asistencias_x_90,
                STRING_AGG(DISTINCT sr.strengths, '; ') AS fortalezas_resumidas,
                STRING_AGG(DISTINCT sr.weaknesses, '; ') AS debilidades_resumidas,
                CASE
                    WHEN MAX(sr.overall_rating) >= 8.0 THEN
                        'Jugador con impacto inmediato. Alto rendimiento estadístico y valoración cualitativa sobresaliente. Perfila como titular competitivo en ligas exigentes.'
                    WHEN MAX(sr.overall_rating) BETWEEN 7.0 AND 7.9 THEN
                        'Jugador con buen rendimiento y proyección. Combina cifras sólidas con evaluación positiva. Puede evolucionar a rol protagónico.'
                    WHEN MAX(sr.overall_rating) BETWEEN 6.0 AND 6.9 THEN
                        'Jugador con condiciones interesantes pero con áreas claras por desarrollar. Potencial para evolucionar según contexto táctico.'
                    ELSE
                        'Perfil con rendimiento limitado según métricas actuales. Requiere seguimiento para evaluar crecimiento.'
                END AS conclusion_profesional
            FROM players p
            LEFT JOIN stats s ON p.player_id = s.player_id
            LEFT JOIN scouting_reports sr ON p.player_id = sr.player_id
            GROUP BY p.player_id, p.full_name, p.position, p.nationality, p.birth_date;
        """)

def sync_to_prod():
    print("\n🔄 Sincronizando BASE DE DESARROLLO → PRODUCCIÓN...\n")

    dev_conn = psycopg2.connect(**DEV_CONFIG)
    prod_conn = psycopg2.connect(**PROD_CONFIG)

    try:
        # 1) Sincronizarestructura
        sync_structure(dev_conn, prod_conn)

        # 2) Copiar datos en orden
        for table in TABLES:
            print(f"📤 Copiando tabla: {table}")

            rows, columns = fetch_all_rows(dev_conn, table)

            truncate_table(prod_conn, table)
            insert_into_table(prod_conn, table, columns, rows)

        prod_conn.commit()
        print("\n✅ Sincronización COMPLETADA sin errores.\n")

    except Exception as e:
        print("\n❌ ERROR durante la sincronización:", e)
        prod_conn.rollback()

    finally:
        dev_conn.close()
        prod_conn.close()

if __name__ == "__main__":
    sync_to_prod()
