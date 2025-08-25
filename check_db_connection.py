#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados
"""

import os
import sys
from urllib.parse import urlparse

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    
    # Testar variáveis de ambiente
    database_url = os.environ.get("DATABASE_URL")
    flask_env = os.environ.get("FLASK_ENV", "development")
    
    print(f"FLASK_ENV: {flask_env}")
    print(f"DATABASE_URL configurada: {'Sim' if database_url else 'Não'}")
    
    if database_url:
        # Parse da URL para mostrar informações (sem senha)
        parsed = urlparse(database_url)
        print(f"Banco: {parsed.scheme}")
        print(f"Host: {parsed.hostname}")
        print(f"Porta: {parsed.port}")
        print(f"Database: {parsed.path[1:] if parsed.path else 'N/A'}")
        print(f"Usuário: {parsed.username}")
    
    # Testar conexão usando SQLAlchemy
    try:
        from src.main import create_app
        
        app = create_app()
        
        with app.app_context():
            from src.models.user import db
            
            # Testar conexão
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1 as test'))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Conexão com banco de dados OK!")
                
                # Listar tabelas
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"Tabelas encontradas: {tables}")
                
                return True
            else:
                print("❌ Falha no teste de conexão")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_database_connection()
    sys.exit(0 if success else 1)

