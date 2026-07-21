import sqlite3

conn = sqlite3.connect("database/chatbot.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM chat_history")

rows = cursor.fetchall()

print("\n===== Chat History =====\n")

for row in rows:
    print(row)

conn.close()