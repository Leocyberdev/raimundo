
#!/usr/bin/env python3
"""
Script para inicializar o banco de dados no Render
"""

import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from flask_migrate import upgrade
from src.main import app
from src.models.user import db, User
from src.models.almoxarifado import Funcionario

def init_render_db():
    """Inicializa o banco de dados no Render"""
    with app.app_context():
        try:
            # Aplica as migrações
            print("Aplicando migrações...")
            upgrade()
            print("Migrações aplicadas com sucesso!")
            
            # Criar usuário admin master se não existir
            admin_user = User.query.filter_by(username="Monter").first()
            if not admin_user:
                admin_user = User(
                    username="Monter",
                    email="admin@sistema.com",
                    tipo_usuario="almoxarifado",
                    ativo=True
                )
                admin_user.set_password("almox")
                db.session.add(admin_user)
                db.session.commit()
                print("Usuário admin master criado: Monter / almox")
            else:
                print("Usuário admin já existe")

            # Criar funcionário padrão se não existir
            funcionario_padrao = Funcionario.query.filter_by(id=1).first()
            if not funcionario_padrao:
                funcionario_padrao = Funcionario(
                    id=1,
                    nome="Sistema",
                    cargo="Operador do Sistema",
                    ativo=True
                )
                db.session.add(funcionario_padrao)
                db.session.commit()
                print("Funcionário padrão criado: Sistema")
            else:
                print("Funcionário padrão já existe")

            print("Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao inicializar banco: {e}")
            sys.exit(1)

if __name__ == '__main__':
    init_render_db()


            # Executa a migração de dados do SQLite para o PostgreSQL
            if os.path.exists(os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')):
                print("Iniciando migração de dados do SQLite para PostgreSQL...")
                try:
                    from src.migrate_sqlite_to_postgres import migrate_sqlite_to_postgres
                    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')
                    postgres_url = os.environ.get("DATABASE_URL")
                    if postgres_url:
                        migrate_sqlite_to_postgres(sqlite_db_path, postgres_url)
                        print("Migração de dados concluída!")
                    else:
                        print("DATABASE_URL não configurada, pulando migração de dados.")
                except Exception as e:
                    print(f"Erro durante a migração de dados: {e}")
            else:
                print("Arquivo app.db (SQLite) não encontrado, pulando migração de dados.")


