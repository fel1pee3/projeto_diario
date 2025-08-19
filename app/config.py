import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Caminho do banco SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'projeto_diario.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'minha_chave_secreta'  # Para segurança em sessões, JWT, etc.
