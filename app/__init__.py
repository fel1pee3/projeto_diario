from flask import Flask
from app.extensions import db, jwt
from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    # Criar todas as tabelas
    with app.app_context():
        db.create_all()

    # Registrar blueprints (rotas)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
