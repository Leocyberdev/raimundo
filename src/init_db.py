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
    env = os.environ.get('FLASK_ENV', 'development')
    print(f"Inicializando banco de dados para ambiente: {env}")
    
    # Cria a aplicação
    app = create_app(env)
    
    with app.app_context():
        # Cria todas as tabelas
        print("Criando tabelas...")
        db.create_all()
        
        # Criar usuário admin master se não existir
        admin_user = User.query.filter_by(username='Monter').first()
        if not admin_user:
            admin_user = User(
                username='Monter',
                email='admin@sistema.com',
                tipo_usuario='almoxarifado',
                is_admin=True,
                ativo=True
            )
            admin_user.set_password('almox')
            db.session.add(admin_user)
            print("Usuário admin master criado: Monter / almox")
        else:
            print("Usuário admin master já existe")

        # Criar funcionário padrão se não existir
        funcionario_padrao = Funcionario.query.filter_by(id=1).first()
        if not funcionario_padrao:
            funcionario_padrao = Funcionario(
                id=1,
                nome='Sistema',
                cargo='Operador do Sistema',
                ativo=True
            )
            db.session.add(funcionario_padrao)
            print("Funcionário padrão criado: Sistema")
        else:
            print("Funcionário padrão já existe")

        # Salva as alterações
        db.session.commit()
        print("Banco de dados inicializado com sucesso!")
        
        # Mostra informações da configuração atual
        print(f"\nConfiguração atual:")
        print(f"- Ambiente: {env}")
        print(f"- Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"- Debug: {app.config.get('DEBUG', False)}")

if __name__ == '__main__':
    init_database()

