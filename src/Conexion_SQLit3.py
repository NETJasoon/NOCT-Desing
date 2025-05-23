from quart import Quart, render_template, request, redirect, url_for, flash
from libsql_client import create_client
from hypercorn.asyncio import serve
from hypercorn.config import Config
import asyncio

app = Quart(__name__)
app.secret_key = 'clave_secreta_para_flash'

@app.before_serving
async def init_db():
    global client
    client = create_client(
        url="https://database-jasongt.aws-ap-northeast-1.turso.io",
        auth_token="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NDgwMTg4MDgsImlkIjoiYzczNTQxMTYtNGM2MC00OTNlLThhMGQtNTE2MDYzZWMzMzNkIiwicmlkIjoiM2RjZDNkZjYtYTdjNS00NmM1LTg5NmQtM2JmZGQxMTliM2UyIn0.pqe1Ry_lex3ddSlloFSJDSczHLfmRIrv6qVsFlF3PCZtehs_S3OyXriTQBwV1NV-cuRRbTIJEhXVuJ9h5Mm9CA"
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

        await client.execute(
            "INSERT INTO contacto (nombre, correo, mensaje) VALUES (?, ?, ?)",
            [nombre, correo, mensaje]
        )
        flash("¡Mensaje enviado correctamente!")
        return redirect(url_for("contacto"))

    return await render_template("contacto.html")

if __name__ == "__main__":
    config = Config()
    config.bind = ["127.0.0.1:3000"]
    asyncio.run(serve(app, config))
