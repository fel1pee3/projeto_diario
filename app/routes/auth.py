from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Registrar usuário
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Usuário já existe'}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    novo_usuario = User(username=username, password=hashed_password.decode('utf-8'))
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'msg': 'Usuário registrado com sucesso!'}), 201

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'msg': 'Usuário ou senha incorretos'}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify({'access_token': access_token}), 200

# Home protegida
@auth_bp.route('/home', methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return jsonify({'msg': f'Bem-vindo, {current_user}!'}), 200

# Logout (opcional, JWT é stateless, mas pode ser feito no frontend)
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'msg': 'Logout realizado!'}), 200
