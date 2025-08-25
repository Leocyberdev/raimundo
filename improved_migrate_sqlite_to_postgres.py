#!/usr/bin/env python3
"""
Script melhorado para migração de dados do SQLite para PostgreSQL
Preserva tipos de dados e estrutura das tabelas usando SQLAlchemy
"""

import os
import sys
from urllib.parse import urlparse
import sqlite3
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

def migrate_sqlite_to_postgres_improved(sqlite_db_path, postgres_url):
    """
    Migra dados do SQLite para PostgreSQL preservando tipos de dados
    """
    print(f"Iniciando migração melhorada de {sqlite_db_path} para PostgreSQL")
    
    if not os.path.exists(sqlite_db_path):
        print(f"Arquivo SQLite não encontrado: {sqlite_db_path}")
        return False
    
    try:
        # Conectar ao SQLite
        sqlite_engine = create_engine(f'sqlite:///{sqlite_db_path}')
        sqlite_metadata = MetaData()
        sqlite_metadata.reflect(bind=sqlite_engine)
        
        # Normalizar URL do PostgreSQL
        if postgres_url.startswith("postgres://"):
            postgres_url = postgres_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif postgres_url.startswith("postgresql://"):
            postgres_url = postgres_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        # Conectar ao PostgreSQL
        postgres_engine = create_engine(postgres_url)
        
        # Criar sessões
        SqliteSession = sessionmaker(bind=sqlite_engine)
        PostgresSession = sessionmaker(bind=postgres_engine)
        
        sqlite_session = SqliteSession()
        postgres_session = PostgresSession()
        
        # Mapear tipos de dados SQLite para PostgreSQL
        type_mapping = {
            'INTEGER': Integer,
            'TEXT': Text,
            'VARCHAR': String,
            'BOOLEAN': Boolean,
            'DATETIME': DateTime,
            'FLOAT': Float,
            'REAL': Float
        }
        
        # Migrar cada tabela
        for table_name in sqlite_metadata.tables:
            print(f"Migrando tabela: {table_name}")
            
            sqlite_table = sqlite_metadata.tables[table_name]
            
            # Obter dados do SQLite
            result = sqlite_session.execute(sqlite_table.select())
            rows = result.fetchall()
            
            if not rows:
                print(f"Tabela {table_name} vazia, pulando.")
                continue
            
            # Conectar diretamente ao PostgreSQL para operações DDL
            pg_conn = psycopg2.connect(postgres_url.replace("postgresql+psycopg2://", "postgresql://"))
            pg_cursor = pg_conn.cursor()
            
            try:
                # Verificar se a tabela já existe
                pg_cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table_name,))
                
                table_exists = pg_cursor.fetchone()[0]
                
                if table_exists:
                    print(f"Tabela {table_name} já existe no PostgreSQL, limpando dados...")
                    pg_cursor.execute(f"DELETE FROM {table_name}")
                else:
                    print(f"Criando tabela {table_name} no PostgreSQL...")
                    # Criar tabela baseada na estrutura do SQLite
                    create_sql = f"CREATE TABLE {table_name} ("
                    columns = []
                    
                    for column in sqlite_table.columns:
                        col_name = column.name
                        col_type = str(column.type).upper()
                        
                        # Mapear tipo
                        if 'VARCHAR' in col_type:
                            pg_type = "TEXT"
                        elif 'INTEGER' in col_type:
                            if column.primary_key:
                                pg_type = "SERIAL PRIMARY KEY"
                            else:
                                pg_type = "INTEGER"
                        elif 'BOOLEAN' in col_type:
                            pg_type = "BOOLEAN"
                        elif 'DATETIME' in col_type:
                            pg_type = "TIMESTAMP"
                        elif 'FLOAT' in col_type or 'REAL' in col_type:
                            pg_type = "FLOAT"
                        else:
                            pg_type = "TEXT"
                        
                        if column.primary_key and 'SERIAL' not in pg_type:
                            pg_type += " PRIMARY KEY"
                        elif not column.nullable and not column.primary_key:
                            pg_type += " NOT NULL"
                        
                        columns.append(f"{col_name} {pg_type}")
                    
                    create_sql += ", ".join(columns) + ")"
                    pg_cursor.execute(create_sql)
                
                pg_conn.commit()
                
                # Inserir dados
                if rows:
                    column_names = [col.name for col in sqlite_table.columns]
                    placeholders = ", ".join(["%s"] * len(column_names))
                    insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
                    
                    for row in rows:
                        # Converter valores None para NULL
                        processed_row = []
                        for value in row:
                            if value is None:
                                processed_row.append(None)
                            elif isinstance(value, bool):
                                processed_row.append(value)
                            else:
                                processed_row.append(value)
                        
                        pg_cursor.execute(insert_sql, processed_row)
                    
                    pg_conn.commit()
                    print(f"Migrados {len(rows)} registros para a tabela {table_name}")
                
            except Exception as e:
                pg_conn.rollback()
                print(f"Erro ao migrar tabela {table_name}: {e}")
                continue
            finally:
                pg_cursor.close()
                pg_conn.close()
        
        sqlite_session.close()
        postgres_session.close()
        
        print("Migração concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        return False

if __name__ == '__main__':
    sqlite_db = os.path.join('src', 'database', 'app.db')
    postgres_url = os.environ.get("DATABASE_URL")
    
    if not postgres_url:
        print("Erro: DATABASE_URL não configurada.")
        sys.exit(1)
    
    success = migrate_sqlite_to_postgres_improved(sqlite_db, postgres_url)
    if not success:
        sys.exit(1)

