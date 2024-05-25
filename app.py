from flask import Flask
from utils.db import db

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lau:2003mayo@localhost/productos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos
    db.init_app(app)

    # Registro de los blueprints
    from routes.products import products
    app.register_blueprint(products)

    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
    return app
