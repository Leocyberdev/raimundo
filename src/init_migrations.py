
#!/usr/bin/env python3
"""
Script para inicializar as migrações do Flask-Migrate
"""

import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask_migrate import init, migrate, upgrade
from src.main import app

def init_migrations():
    """Inicializa o sistema de migrações"""
    with app.app_context():
        try:
            # Tenta fazer upgrade das migrações existentes
            upgrade()
            print("Migrações aplicadas com sucesso!")
        except Exception as e:
            print(f"Erro ao aplicar migrações: {e}")
            print("Tentando inicializar o sistema de migrações...")
            
            # Se falhar, tenta inicializar
            try:
                init()
                print("Sistema de migrações inicializado!")
                
                # Cria a primeira migração
                migrate(message="Initial migration")
                print("Migração inicial criada!")
                
                # Aplica a migração
                upgrade()
                print("Migração aplicada com sucesso!")
                
            except Exception as e2:
                print(f"Erro ao inicializar migrações: {e2}")

if __name__ == '__main__':
    init_migrations()
