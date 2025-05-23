from quart import Quart, render_template, request, redirect, url_for, flash
from libsql_client import create_client
from hypercorn.asyncio import serve
from hypercorn.config import Config
import asyncio
import os
import re

app = Quart(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_para_flash")

@app.before_serving
async def init_db():
    global client
    client = create_client(
        url=os.getenv("TURSO_URL"),
        auth_token=os.getenv("TURSO_TOKEN")
    )
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

        if not nombre or not correo or not mensaje:
            flash("Por favor, completa todos los campos.", "error")
            return redirect(url_for("contacto"))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            flash("Correo electrónico inválido.", "error")
            return redirect(url_for("contacto"))

        await client.execute(
            "INSERT INTO contacto (nombre, correo, mensaje) VALUES (?, ?, ?)",
            [nombre, correo, mensaje]
        )
        flash("¡Mensaje enviado correctamente!", "success")
        return redirect(url_for("contacto"))

    return await render_template("contacto.html")

if __name__ == "__main__":
    config = Config()
    config.bind = [f"0.0.0.0:{os.getenv('PORT', '10000')}"]  # Render asigna el puerto dinámicamente
    asyncio.run(serve(app, config))
