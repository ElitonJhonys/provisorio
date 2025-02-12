from flask import Flask
from routes import init_routes
import database

app = Flask(__name__)
app.config.from_object("config")  # Importa configurações do arquivo config.py

# Inicializa o banco de dados e as rotas
database.init_db()
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
