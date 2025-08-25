
import sqlite3
import os
import psycopg2
from urllib.parse import urlparse

def migrate_sqlite_to_postgres(sqlite_db_path, postgres_url):
    print(f"Iniciando migração de {sqlite_db_path} para {postgres_url}")

    # Conectar ao SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()

    # Conectar ao PostgreSQL
    try:
        result = urlparse(postgres_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port

        pg_conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return

    # Obter lista de tabelas do SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type=\'table\';")
    tables = sqlite_cursor.fetchall()

    for table_name in tables:
        table_name = table_name[0]
        print(f"Migrando tabela: {table_name}")

        # Obter dados do SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()

        if not rows:
            print(f"Tabela {table_name} vazia, pulando.")
            continue

        # Obter nomes das colunas do SQLite
        column_names = [description[0] for description in sqlite_cursor.description]

        # Criar tabela no PostgreSQL (se não existir) e inserir dados
        # Nota: Esta é uma abordagem simplificada. Em um cenário real, você precisaria
        # mapear tipos de dados e lidar com chaves primárias/estrangeiras.
        try:
            # Drop table if exists (for testing purposes)
            pg_cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            pg_conn.commit()

            # Create table statement (simplified)
            create_table_sql = f"CREATE TABLE {table_name} (\n"
            for col_name in column_names:
                create_table_sql += f"    {col_name} TEXT,\n" # Usando TEXT para simplificar, ajustar conforme necessário
            create_table_sql = create_table_sql.rstrip(",\n") + "\n);"
            pg_cursor.execute(create_table_sql)
            pg_conn.commit()
            print(f"Tabela {table_name} criada no PostgreSQL.")

            # Inserir dados
            placeholders = ", ".join(["%s"] * len(column_names))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
            for row in rows:
                pg_cursor.execute(insert_sql, row)
            pg_conn.commit()
            print(f"Dados da tabela {table_name} migrados com sucesso.")

        except Exception as e:
            pg_conn.rollback()
            print(f"Erro ao migrar tabela {table_name}: {e}")

    sqlite_conn.close()
    pg_conn.close()
    print("Migração concluída!")

if __name__ == '__main__':
    sqlite_db = os.path.join('src', 'database', 'app.db')
    postgres_conn_str = "postgresql://almoxarifado_user:3f1Fejooy5H0h5GN8kKdX9oIt6Mq3LIp@dpg-d2lisv7diees73c32ad0-a/almoxarifado"
    migrate_sqlite_to_postgres(sqlite_db, postgres_conn_str)


