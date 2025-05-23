
from quart import Quart, render_template, request, redirect, url_for, flash
from libsql_client import create_client
import os

app = Quart(__name__)
app.secret_key = 'clave_secreta_para_flash'

client = create_client(
    url=os.getenv("TURSO_URL"),
    auth_token=os.getenv("TURSO_TOKEN")
)

@app.before_serving
async def init_db():
    await client.execute("""
    CREATE TABLE IF NOT EXISTS contacto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT,
        mensaje TEXT
    )
    """)

@app.route("/contacto", methods=["GET", "POST"])
async def contacto():
    if request.method == "POST":
        form = await request.form
        nombre = form.get("nombre")
        correo = form.get("correo")
        mensaje = form.get("mensaje")

        await client.execute(
            "INSERT INTO contacto (nombre, correo, mensaje) VALUES (?, ?, ?)",
            [nombre, correo, mensaje]
        )
        flash("¡Mensaje enviado correctamente!")
        return redirect(url_for("contacto"))

    return await render_template("contacto.html")
