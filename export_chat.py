import sqlite3
import csv

DB_NAME = "database/chatbot.db"


def export_chat_history():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chat_history")

    rows = cursor.fetchall()

    conn.close()

    with open("chat_history.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Role",
            "Message"
        ])

        writer.writerows(rows)

    print("Chat history exported successfully!")


if __name__ == "__main__":
    export_chat_history()