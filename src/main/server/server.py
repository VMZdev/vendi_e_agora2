import os
from flask import Flask
from flask_cors import CORS
from src.models.sqlite.settings.connection import db_connection_handler
from dotenv import load_dotenv
load_dotenv()


# importar blueprints
from src.main.routes.customer_routes import customer_route_bp
from src.main.routes.product_routes import product_route_bp
from src.main.routes.historico_routes import historico_route_bp
from src.main.routes.analysis_routes import graphs_route_bp
from src.main.routes.home_route import home_route_bp
from src.main.routes.uploads_routes import upload_route_bp
from src.main.routes.exports_routes import exports_route_bp
from src.main.routes.auth_routes import auth_route_bp


from src.models.sqlite.settings.base import Base
from src.models.sqlite.entitites.user import UserTable
from src.models.sqlite.entitites.historico_de_vendas import HistoricoDeVendasTable
from src.models.sqlite.entitites.customer import CustomerTable
from src.models.sqlite.entitites.products import ProductTable
from src.models.sqlite.entitites.uploads import UploadsTable



# Conectar ao banco de dados
db_connection_handler.connect_to_db()

# Configuração do app Flask
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'static'))
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)

# Registro de blueprints
app.register_blueprint(customer_route_bp)
app.register_blueprint(product_route_bp)
app.register_blueprint(historico_route_bp)
app.register_blueprint(graphs_route_bp)
app.register_blueprint(home_route_bp)
app.register_blueprint(upload_route_bp)
app.register_blueprint(exports_route_bp)
app.register_blueprint(auth_route_bp)

Base.metadata.create_all(db_connection_handler.get_engine())