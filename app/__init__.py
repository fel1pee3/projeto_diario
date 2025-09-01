from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_migrate import Migrate
from app.extensions import db, jwt
from app.models.user import User
from app.models.note import Note
from app.routes.auth import auth_bp
from app.routes.notes import notes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    # Configurar migrate
    migrate = Migrate(app, db)

    # Criar todas as tabelas
    with app.app_context():
        db.create_all()

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    # Rota principal - redireciona conforme autenticação
    @app.route('/')
    def index():
        return redirect(url_for('home'))

    # Rota de home protegida
    @app.route('/home')
    def home():
        return render_template('home.html')

    # Rota de login
    @app.route('/login')
    def login_page():
        return render_template('login.html')

    # Rota de registro
    @app.route('/register')
    def register_page():
        return render_template('register.html')

    return app