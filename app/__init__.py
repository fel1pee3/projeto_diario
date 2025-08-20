from flask import Flask
from flask_migrate import Migrate
from app.extensions import db, jwt
from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    # Configurar migrate
    migrate = Migrate(app, db)

    # Criar todas as tabelas (opcional, você pode usar migrate)
    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
