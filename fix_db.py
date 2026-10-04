import sqlite3

conn = sqlite3.connect("waste_segregation.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE predictions ADD COLUMN instruction TEXT;")
    print("Column added successfully")
except Exception as e:
    print("Already exists or error:", e)

conn.commit()
conn.close()