from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.note import Note

app = create_app()

with app.app_context():
    # Criar todas as tabelas
    db.create_all()
    print("Tabelas criadas com sucesso!")
    print("Tabelas disponíveis:")
    for table in db.metadata.tables:
        print(f"- {table}")
