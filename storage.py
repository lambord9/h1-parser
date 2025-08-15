import psycopg2
from config import PG_HOST, PG_PORT, PG_DATABASE, PG_USER, PG_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sent_reports (
            report_id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            reporter TEXT,
            severity TEXT,
            team TEXT,
            award NUMERIC,
            created TIMESTAMP,
            disclosed TIMESTAMP,
            saved_at TIMESTAMP DEFAULT now()
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


def is_new_report(report_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM sent_reports WHERE report_id = %s", (report_id,))
    exists = cur.fetchone()
    cur.close()
    conn.close()
    return not exists


def save_report(report):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO sent_reports (report_id, title, url, reporter, severity, team, award, created, disclosed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (report_id) DO NOTHING
        """,
        (
            report["id"],
            report["title"],
            report["url"],
            report["reporter"],
            report["severity"],
            report["team"],
            report["award"],
            report["created"],
            report["disclosed"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


def is_db_empty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sent_reports")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count == 0
