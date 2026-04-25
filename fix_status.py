import sqlite3

conn = sqlite3.connect("rent.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE listings ADD COLUMN status TEXT DEFAULT 'active'")

conn.commit()
conn.close()

print("status column added successfully")