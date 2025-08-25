#!/usr/bin/env python3
"""
Script para migrar dados do SQLite para PostgreSQL no Render
"""

import sqlite3
import psycopg2
import os
import sys
from urllib.parse import urlparse

def conectar_sqlite(caminho_db):
    """Conecta ao banco SQLite local"""
    try:
        conn = sqlite3.connect(caminho_db)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        return conn
    except Exception as e:
        print(f"Erro ao conectar SQLite: {e}")
        return None

def conectar_postgresql(database_url):
    """Conecta ao banco PostgreSQL no Render"""
    try:
        # Parse da URL do banco
        url = urlparse(database_url)
        
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],  # Remove a barra inicial
            user=url.username,
            password=url.password
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar PostgreSQL: {e}")
        return None

def migrar_usuarios(sqlite_conn, pg_conn):
    """Migra usuários do SQLite para PostgreSQL"""
    print("Migrando usuários...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Buscar usuários do SQLite
    sqlite_cursor.execute("SELECT * FROM users")
    usuarios = sqlite_cursor.fetchall()
    
    for usuario in usuarios:
        try:
            # Verificar se usuário já existe no PostgreSQL
            pg_cursor.execute("SELECT id FROM users WHERE username = %s", (usuario['username'],))
            if pg_cursor.fetchone():
                print(f"Usuário {usuario['username']} já existe, pulando...")
                continue
            
            # Inserir usuário no PostgreSQL
            pg_cursor.execute("""
                INSERT INTO users (username, email, password_hash, tipo_usuario, ativo, data_criacao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                usuario['username'],
                usuario['email'],
                usuario['password_hash'],
                usuario['tipo_usuario'],
                usuario['ativo'],
                usuario['data_criacao']
            ))
            print(f"Usuário {usuario['username']} migrado com sucesso")
            
        except Exception as e:
            print(f"Erro ao migrar usuário {usuario['username']}: {e}")
    
    pg_conn.commit()

def migrar_funcionarios(sqlite_conn, pg_conn):
    """Migra funcionários do SQLite para PostgreSQL"""
    print("Migrando funcionários...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Buscar funcionários do SQLite
    sqlite_cursor.execute("SELECT * FROM funcionarios")
    funcionarios = sqlite_cursor.fetchall()
    
    for funcionario in funcionarios:
        try:
            # Verificar se funcionário já existe no PostgreSQL
            pg_cursor.execute("SELECT id FROM funcionarios WHERE nome = %s", (funcionario['nome'],))
            if pg_cursor.fetchone():
                print(f"Funcionário {funcionario['nome']} já existe, pulando...")
                continue
            
            # Inserir funcionário no PostgreSQL
            pg_cursor.execute("""
                INSERT INTO funcionarios (nome, cargo, ativo, data_criacao)
                VALUES (%s, %s, %s, %s)
            """, (
                funcionario['nome'],
                funcionario['cargo'],
                funcionario['ativo'],
                funcionario['data_criacao']
            ))
            print(f"Funcionário {funcionario['nome']} migrado com sucesso")
            
        except Exception as e:
            print(f"Erro ao migrar funcionário {funcionario['nome']}: {e}")
    
    pg_conn.commit()

def migrar_categorias(sqlite_conn, pg_conn):
    """Migra categorias do SQLite para PostgreSQL"""
    print("Migrando categorias...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Buscar categorias do SQLite
    sqlite_cursor.execute("SELECT * FROM categorias")
    categorias = sqlite_cursor.fetchall()
    
    for categoria in categorias:
        try:
            # Verificar se categoria já existe no PostgreSQL
            pg_cursor.execute("SELECT id FROM categorias WHERE nome = %s", (categoria['nome'],))
            if pg_cursor.fetchone():
                print(f"Categoria {categoria['nome']} já existe, pulando...")
                continue
            
            # Inserir categoria no PostgreSQL
            pg_cursor.execute("""
                INSERT INTO categorias (nome, descricao, ativa, data_criacao)
                VALUES (%s, %s, %s, %s)
            """, (
                categoria['nome'],
                categoria['descricao'],
                categoria['ativa'],
                categoria['data_criacao']
            ))
            print(f"Categoria {categoria['nome']} migrada com sucesso")
            
        except Exception as e:
            print(f"Erro ao migrar categoria {categoria['nome']}: {e}")
    
    pg_conn.commit()

def migrar_fornecedores(sqlite_conn, pg_conn):
    """Migra fornecedores do SQLite para PostgreSQL"""
    print("Migrando fornecedores...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Buscar fornecedores do SQLite
    sqlite_cursor.execute("SELECT * FROM fornecedores")
    fornecedores = sqlite_cursor.fetchall()
    
    for fornecedor in fornecedores:
        try:
            # Verificar se fornecedor já existe no PostgreSQL
            pg_cursor.execute("SELECT id FROM fornecedores WHERE nome = %s", (fornecedor['nome'],))
            if pg_cursor.fetchone():
                print(f"Fornecedor {fornecedor['nome']} já existe, pulando...")
                continue
            
            # Inserir fornecedor no PostgreSQL
            pg_cursor.execute("""
                INSERT INTO fornecedores (nome, ativo, data_criacao)
                VALUES (%s, %s, %s)
            """, (
                fornecedor['nome'],
                fornecedor['ativo'],
                fornecedor['data_criacao']
            ))
            print(f"Fornecedor {fornecedor['nome']} migrado com sucesso")
            
        except Exception as e:
            print(f"Erro ao migrar fornecedor {fornecedor['nome']}: {e}")
    
    pg_conn.commit()

def migrar_obras(sqlite_conn, pg_conn):
    """Migra obras do SQLite para PostgreSQL"""
    print("Migrando obras...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Buscar obras do SQLite
    sqlite_cursor.execute("SELECT * FROM obras")
    obras = sqlite_cursor.fetchall()
    
    for obra in obras:
        try:
            # Verificar se obra já existe no PostgreSQL
            pg_cursor.execute("SELECT id FROM obras WHERE nome = %s", (obra['nome'],))
            if pg_cursor.fetchone():
                print(f"Obra {obra['nome']} já existe, pulando...")
                continue
            
            # Inserir obra no PostgreSQL
            pg_cursor.execute("""
                INSERT INTO obras (nome, descricao, ativa, data_criacao)
                VALUES (%s, %s, %s, %s)
            """, (
                obra['nome'],
                obra['descricao'],
                obra['ativa'],
                obra['data_criacao']
            ))
            print(f"Obra {obra['nome']} migrada com sucesso")
            
        except Exception as e:
            print(f"Erro ao migrar obra {obra['nome']}: {e}")
    
    pg_conn.commit()

def migrar_produtos(sqlite_conn, pg_conn):
    """Migra produtos do SQLite para PostgreSQL"""
    print("Migrando produtos...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Buscar produtos do SQLite
    sqlite_cursor.execute("SELECT * FROM produtos")
    produtos = sqlite_cursor.fetchall()
    
    for produto in produtos:
        try:
            # Verificar se produto já existe no PostgreSQL
            pg_cursor.execute("SELECT id FROM produtos WHERE nome = %s", (produto['nome'],))
            if pg_cursor.fetchone():
                print(f"Produto {produto['nome']} já existe, pulando...")
                continue
            
            # Inserir produto no PostgreSQL
            pg_cursor.execute("""
                INSERT INTO produtos (nome, descricao, categoria, fornecedor, preco, 
                                    quantidade_estoque, unidade_medida, ativo, data_criacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                produto['nome'],
                produto['descricao'],
                produto['categoria'],
                produto['fornecedor'],
                produto['preco'],
                produto['quantidade_estoque'],
                produto['unidade_medida'],
                produto['ativo'],
                produto['data_criacao']
            ))
            print(f"Produto {produto['nome']} migrado com sucesso")
            
        except Exception as e:
            print(f"Erro ao migrar produto {produto['nome']}: {e}")
    
    pg_conn.commit()

def main():
    """Função principal de migração"""
    # Verificar argumentos
    if len(sys.argv) != 3:
        print("Uso: python script_migracao.py <caminho_sqlite> <url_postgresql>")
        print("Exemplo: python script_migracao.py ./src/database/app.db postgresql://user:pass@host:port/db")
        sys.exit(1)
    
    caminho_sqlite = sys.argv[1]
    url_postgresql = sys.argv[2]
    
    # Verificar se arquivo SQLite existe
    if not os.path.exists(caminho_sqlite):
        print(f"Arquivo SQLite não encontrado: {caminho_sqlite}")
        sys.exit(1)
    
    # Conectar aos bancos
    print("Conectando aos bancos de dados...")
    sqlite_conn = conectar_sqlite(caminho_sqlite)
    if not sqlite_conn:
        sys.exit(1)
    
    pg_conn = conectar_postgresql(url_postgresql)
    if not pg_conn:
        sqlite_conn.close()
        sys.exit(1)
    
    try:
        # Executar migrações na ordem correta (respeitando dependências)
        migrar_usuarios(sqlite_conn, pg_conn)
        migrar_funcionarios(sqlite_conn, pg_conn)
        migrar_categorias(sqlite_conn, pg_conn)
        migrar_fornecedores(sqlite_conn, pg_conn)
        migrar_obras(sqlite_conn, pg_conn)
        migrar_produtos(sqlite_conn, pg_conn)
        
        print("\n✅ Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {e}")
        pg_conn.rollback()
    
    finally:
        # Fechar conexões
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    main()

