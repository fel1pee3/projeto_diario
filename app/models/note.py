from app.extensions import db
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    
    # Relacionamento com usuário
    user = db.relationship('User', backref=db.backref('notes', lazy=True))

    def __repr__(self):
        return f'<Note {self.title}>'
