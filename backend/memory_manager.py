import sqlite3

DB_NAME = "memory.db"

def save_message(role, message):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT
        )
    """)

    cur.execute(
        "INSERT INTO memory (role, message) VALUES (?, ?)",
        (role, message)
    )

    conn.commit()
    conn.close()


def get_conversation():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT role, message FROM memory")
    rows = cur.fetchall()

    conn.close()
    return rows
