import sqlite3

DB_NAME = "database/chatbot.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
    conn.commit()
    conn.close()
def save_message(role, message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO chat_history(role, message)
        VALUES(?,?)
        """,
        (role, message)
    )

    conn.commit()
    conn.close()


def load_chat_history():

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM chat_history"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_chat_history():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()

def search_chat_history(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM chat_history
        WHERE message LIKE ?
        """,
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows