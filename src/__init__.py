from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/quickly_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar modelos para que SQLAlchemy cree ambas tablas en MySQL
    from src.models.categoria import Categoria
    from src.models.producto import Producto
    with app.app_context():
        db.create_all()

    # Registrar las rutas de ambos módulos
    from src.routes.categoria_routes import categoria_bp
    from src.routes.producto_routes import producto_bp
    app.register_blueprint(categoria_bp)
    app.register_blueprint(producto_bp)

    return app
