from flask import Flask
from flask_cors import CORS
from src.models.sqlite.settings.connection import db_connection_handler

# importar blueprints
from src.main.routes.customer_routes import customer_route_bp
from src.main.routes.product_routes import product_route_bp
from src.main.routes.historico_routes import historico_route_bp

db_connection_handler.connect_to_db()

app = Flask(__name__)
CORS(app)

app.register_blueprint(customer_route_bp) # Registrar as rotas de todas que estão no "pets_route" (Padronizar)
app.register_blueprint(product_route_bp)
app.register_blueprint(historico_route_bp)
