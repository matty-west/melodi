import sqlite3

conn = sqlite3.connect('melodi.db')  # Replace 'your_database.db' with your database file name
cursor = conn.cursor()

sql_code = """
ALTER TABLE songs ADD COLUMN popularity INTEGER;
"""

cursor.execute(sql_code)
conn.commit()
conn.close()