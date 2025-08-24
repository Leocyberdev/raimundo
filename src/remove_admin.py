
#!/usr/bin/env python3

import sqlite3
import os

def main():
    """Remove a coluna is_admin da tabela users"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a coluna is_admin existe
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("Removendo coluna is_admin...")
            
            # Criar nova tabela sem is_admin
            cursor.execute('''
                CREATE TABLE users_new (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'almoxarifado',
                    ativo BOOLEAN DEFAULT 1,
                    data_cadastro DATETIME
                )
            ''')
            
            # Copiar dados da tabela antiga para a nova
            cursor.execute('''
                INSERT INTO users_new (id, username, email, password_hash, tipo_usuario, ativo, data_cadastro)
                SELECT id, username, email, password_hash, tipo_usuario, ativo, data_cadastro
                FROM users
            ''')
            
            # Remover tabela antiga e renomear a nova
            cursor.execute('DROP TABLE users')
            cursor.execute('ALTER TABLE users_new RENAME TO users')
            
            conn.commit()
            print("Coluna is_admin removida com sucesso!")
        else:
            print("Coluna is_admin não encontrada!")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao migrar banco: {e}")

if __name__ == '__main__':
    main()
