import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contacto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    mensaje TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Base de datos inicializada correctamente.")
