import sqlite3
import os

def migrate_database():
    """Adicionar coluna unidade_medida à tabela produtos e criar tabela requisicoes"""
    db_path = os.path.join('src', 'database', 'app.db')

    if not os.path.exists(db_path):
        print("Banco de dados não encontrado!")
        return

    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se a coluna unidade_medida já existe e adicionar se necessário
        cursor.execute("PRAGMA table_info(produtos)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'unidade_medida' not in columns:
            print("Adicionando coluna unidade_medida...")
            cursor.execute("ALTER TABLE produtos ADD COLUMN unidade_medida TEXT DEFAULT 'unidade'")
            print("Coluna unidade_medida adicionada!")
        else:
            print("Coluna unidade_medida já existe!")

        # Criar tabela de requisições se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requisicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                obra_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                quantidade_solicitada REAL NOT NULL,
                quantidade_atendida REAL DEFAULT 0.0,
                status VARCHAR(20) DEFAULT 'PENDENTE',
                data_requisicao DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_atendimento DATETIME,
                observacoes TEXT,
                observacoes_atendimento TEXT,
                atendido_por INTEGER,
                FOREIGN KEY (produto_id) REFERENCES produtos (id),
                FOREIGN KEY (obra_id) REFERENCES obras (id),
                FOREIGN KEY (atendido_por) REFERENCES funcionarios (id)
            )
        ''')
        print("Tabela requisicoes criada/verificada!")

        conn.commit()
        conn.close()
        print("Migração concluída!")

    except Exception as e:
        print(f"Erro na migração: {e}")

if __name__ == '__main__':
    migrate_database()