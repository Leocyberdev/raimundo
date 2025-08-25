#!/usr/bin/env python3
"""
Script melhorado para inicializar o banco de dados no Render
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
            print("=== Inicializando banco de dados no Render ===")
            
            # Verificar se é primeira execução (banco vazio)
            try:
                # Tentar fazer uma consulta simples para verificar se as tabelas existem
                db.session.execute('SELECT 1')
                tables_exist = True
                print("Tabelas já existem no banco de dados")
            except Exception:
                tables_exist = False
                print("Banco de dados vazio, criando estrutura...")
            
            # Se as tabelas não existem, aplicar migrações
            if not tables_exist:
                print("Aplicando migrações do Alembic...")
                try:
                    upgrade()
                    print("Migrações aplicadas com sucesso!")
                except Exception as e:
                    print(f"Erro ao aplicar migrações: {e}")
                    # Se falhar, criar tabelas diretamente
                    print("Criando tabelas diretamente...")
                    db.create_all()
                    print("Tabelas criadas com sucesso!")
            
            # Executar migração de dados do SQLite se o arquivo existir
            sqlite_db_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')
            if os.path.exists(sqlite_db_path):
                print("Arquivo SQLite encontrado, iniciando migração de dados...")
                try:
                    from improved_migrate_sqlite_to_postgres import migrate_sqlite_to_postgres_improved
                    postgres_url = os.environ.get("DATABASE_URL")
                    if postgres_url:
                        success = migrate_sqlite_to_postgres_improved(sqlite_db_path, postgres_url)
                        if success:
                            print("Migração de dados concluída com sucesso!")
                        else:
                            print("Falha na migração de dados, continuando com inicialização padrão...")
                    else:
                        print("DATABASE_URL não configurada, pulando migração de dados.")
                except Exception as e:
                    print(f"Erro durante a migração de dados: {e}")
                    print("Continuando com inicialização padrão...")
            else:
                print("Arquivo SQLite não encontrado, pulando migração de dados.")
            
            # Criar usuário admin master se não existir
            try:
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
            except Exception as e:
                print(f"Erro ao criar usuário admin: {e}")

            # Criar funcionário padrão se não existir
            try:
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
            except Exception as e:
                print(f"Erro ao criar funcionário padrão: {e}")

            print("=== Inicialização do banco de dados concluída ===")
            
        except Exception as e:
            print(f"Erro crítico ao inicializar banco: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    init_render_db()

