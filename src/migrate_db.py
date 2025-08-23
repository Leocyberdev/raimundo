
import sqlite3
import os

def migrate_database():
    """Adicionar coluna unidade_medida à tabela produtos"""
    db_path = os.path.join('src', 'database', 'app.db')
    
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado!")
        return
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(produtos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'unidade_medida' not in columns:
            print("Adicionando coluna unidade_medida...")
            cursor.execute("ALTER TABLE produtos ADD COLUMN unidade_medida TEXT DEFAULT 'unidade'")
            conn.commit()
            print("Coluna unidade_medida adicionada com sucesso!")
        else:
            print("Coluna unidade_medida já existe!")
        
        conn.close()
        print("Migração concluída!")
        
    except Exception as e:
        print(f"Erro na migração: {e}")

if __name__ == '__main__':
    migrate_database()
