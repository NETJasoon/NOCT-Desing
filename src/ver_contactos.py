import sqlite3

try:
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacto")
    registros = cursor.fetchall()

    if registros:
        for r in registros:
            print(r)
    else:
        print("No se encontraron registros en la tabla 'contacto'.")

except sqlite3.Error as e:
    print(f"Error al acceder a la base de datos: {e}")
finally:
    if conn:
        conn.close()
