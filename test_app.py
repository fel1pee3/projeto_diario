try:
    from app import create_app
    print("✓ Importação da aplicação bem-sucedida")
    
    app = create_app()
    print("✓ Aplicação criada com sucesso")
    
    with app.app_context():
        from app.extensions import db
        from app.models.user import User
        from app.models.note import Note
        
        print("✓ Modelos importados com sucesso")
        
        # Criar tabelas
        db.create_all()
        print("✓ Tabelas criadas com sucesso")
        
        # Listar tabelas
        print("Tabelas disponíveis:")
        for table in db.metadata.tables:
            print(f"  - {table}")
            
except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()
