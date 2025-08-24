
#!/usr/bin/env python3
"""
Script para inicializar o banco de dados e criar dados iniciais
Funciona tanto para SQLite (desenvolvimento) quanto PostgreSQL (produção)
"""

import os
import sys

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import create_app
from src.models.user import db, User
from src.models.almoxarifado import Funcionario

def init_database():
    """Inicializa o banco de dados e cria dados iniciais"""
    
    # Detecta o ambiente
    env = os.environ.get("FLASK_ENV", "development")
    print(f"[DEBUG] Inicializando banco de dados para ambiente: {env}")
    
    # Cria a aplicação
    app = create_app(env)
    
    with app.app_context():
        try:
            # Cria todas as tabelas
            print("[DEBUG] Criando tabelas...")
            db.create_all()
            print("[DEBUG] Tabelas criadas com sucesso.")

            # Criar usuário admin master se não existir
            print("[DEBUG] Verificando usuário admin master...")
            admin_user = User.query.filter_by(username="Monter").first()
            if not admin_user:
                admin_user = User(
                    username="Monter",
                    email="admin@sistema.com",
                    tipo_usuario="almoxarifado",
                    is_admin=True,
                    ativo=True
                )
                admin_user.set_password("almox")
                db.session.add(admin_user)
                print("[DEBUG] Usuário admin master \'Monter\' adicionado à sessão.")
            else:
                print("[DEBUG] Usuário admin master \'Monter\' já existe.")

            # Criar funcionário padrão se não existir
            print("[DEBUG] Verificando funcionário padrão...")
            funcionario_padrao = Funcionario.query.filter_by(id=1).first()
            if not funcionario_padrao:
                funcionario_padrao = Funcionario(
                    id=1,
                    nome="Sistema",
                    cargo="Operador do Sistema",
                    ativo=True
                )
                db.session.add(funcionario_padrao)
                print("[DEBUG] Funcionário padrão \'Sistema\' adicionado à sessão.")
            else:
                print("[DEBUG] Funcionário padrão \'Sistema\' já existe.")

            # Salva as alterações
            print("[DEBUG] Commitando alterações no banco de dados...")
            db.session.commit()
            print("[DEBUG] Banco de dados inicializado com sucesso e alterações salvas!")
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERRO] Erro durante a inicialização do banco de dados: {e}")
            sys.exit(1) # Sai com erro

        # Mostra informações da configuração atual
        print(f"\n[DEBUG] Configuração atual:")
        print(f"- Ambiente: {env}")
        print(f"- Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}")
        print(f"- Debug: {app.config.get("DEBUG", False)}")

if __name__ == '__main__':
    init_database()



