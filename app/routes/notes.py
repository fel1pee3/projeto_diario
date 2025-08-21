from flask import Blueprint, request, jsonify, render_template
from app.extensions import db
from app.models.note import Note
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

# Rotas para renderizar templates HTML
@notes_bp.route('/list')
def list_notes_page():
    return render_template('notes/list.html')

@notes_bp.route('/create')
def create_note_page():
    return render_template('notes/create.html')

@notes_bp.route('/view/<int:note_id>')
def view_note_page(note_id):
    return render_template('notes/view.html')

@notes_bp.route('/edit/<int:note_id>')
def edit_note_page(note_id):
    return render_template('notes/edit.html')

# Criar anotação
@notes_bp.route('/', methods=['POST'])
@jwt_required()
def create_note():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'msg': 'Título e conteúdo são obrigatórios'}), 400
    
    nova_anotacao = Note(
        title=title,
        content=content,
        user_id=user.id
    )
    
    db.session.add(nova_anotacao)
    db.session.commit()
    
    return jsonify({
        'msg': 'Anotação criada com sucesso!',
        'note': {
            'id': nova_anotacao.id,
            'title': nova_anotacao.title,
            'content': nova_anotacao.content,
            'created_at': nova_anotacao.created_at.isoformat()
        }
    }), 201

# Listar todas as anotações do usuário
@notes_bp.route('/', methods=['GET'])
@jwt_required()
def list_notes():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    anotacoes = Note.query.filter_by(user_id=user.id).order_by(Note.created_at.desc()).all()
    
    notes_list = []
    for anotacao in anotacoes:
        notes_list.append({
            'id': anotacao.id,
            'title': anotacao.title,
            'content': anotacao.content[:100] + '...' if len(anotacao.content) > 100 else anotacao.content,
            'created_at': anotacao.created_at.isoformat(),
            'updated_at': anotacao.updated_at.isoformat()
        })
    
    return jsonify({'notes': notes_list}), 200

# Visualizar uma anotação individual
@notes_bp.route('/<int:note_id>', methods=['GET'])
@jwt_required()
def view_note(note_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    anotacao = Note.query.filter_by(id=note_id, user_id=user.id).first()
    
    if not anotacao:
        return jsonify({'msg': 'Anotação não encontrada'}), 404
    
    return jsonify({
        'note': {
            'id': anotacao.id,
            'title': anotacao.title,
            'content': anotacao.content,
            'created_at': anotacao.created_at.isoformat(),
            'updated_at': anotacao.updated_at.isoformat()
        }
    }), 200

# Editar uma anotação existente
@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def edit_note(note_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    anotacao = Note.query.filter_by(id=note_id, user_id=user.id).first()
    
    if not anotacao:
        return jsonify({'msg': 'Anotação não encontrada'}), 404
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'msg': 'Título e conteúdo são obrigatórios'}), 400
    
    anotacao.title = title
    anotacao.content = content
    
    db.session.commit()
    
    return jsonify({
        'msg': 'Anotação atualizada com sucesso!',
        'note': {
            'id': anotacao.id,
            'title': anotacao.title,
            'content': anotacao.content,
            'updated_at': anotacao.updated_at.isoformat()
        }
    }), 200

# Deletar uma anotação
@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    anotacao = Note.query.filter_by(id=note_id, user_id=user.id).first()
    
    if not anotacao:
        return jsonify({'msg': 'Anotação não encontrada'}), 404
    
    db.session.delete(anotacao)
    db.session.commit()
    
    return jsonify({'msg': 'Anotação deletada com sucesso!'}), 200
