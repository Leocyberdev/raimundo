#!/usr/bin/env python3
"""
Script melhorado para inicializar o banco de dados no Render
Inclui validações robustas e criação de dados essenciais
"""

import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from flask_migrate import upgrade
from src.main import app
from src.models.user import db, User
from src.models.almoxarifado import Funcionario, Categoria, Fornecedor, Obra

def criar_usuario_admin():
    """Cria usuário admin master se não existir"""
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
            print("✅ Usuário admin master criado: Monter / almox")
        else:
            print("ℹ️  Usuário admin já existe")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        return False

def criar_funcionario_sistema():
    """Cria funcionário padrão do sistema se não existir"""
    try:
        funcionario_sistema = Funcionario.query.filter_by(nome="Sistema").first()
        if not funcionario_sistema:
            funcionario_sistema = Funcionario(
                nome="Sistema",
                cargo="Operador do Sistema",
                ativo=True
            )
            db.session.add(funcionario_sistema)
            db.session.commit()
            print("✅ Funcionário Sistema criado")
        else:
            print("ℹ️  Funcionário Sistema já existe")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar funcionário Sistema: {e}")
        return False

def criar_dados_basicos():
    """Cria categorias, fornecedores e obras básicas se não existirem"""
    try:
        # Categorias básicas
        categorias_basicas = [
            {"nome": "Geral", "descricao": "Categoria geral para produtos diversos"},
            {"nome": "Elétrico", "descricao": "Materiais elétricos"},
            {"nome": "Mecânico", "descricao": "Materiais mecânicos"}
        ]
        
        for cat_data in categorias_basicas:
            categoria = Categoria.query.filter_by(nome=cat_data["nome"]).first()
            if not categoria:
                categoria = Categoria(
                    nome=cat_data["nome"],
                    descricao=cat_data["descricao"],
                    ativa=True
                )
                db.session.add(categoria)
        
        # Fornecedor padrão
        fornecedor_padrao = Fornecedor.query.filter_by(nome="Fornecedor Padrão").first()
        if not fornecedor_padrao:
            fornecedor_padrao = Fornecedor(
                nome="Fornecedor Padrão",
                ativo=True
            )
            db.session.add(fornecedor_padrao)
        
        # Obra padrão
        obra_padrao = Obra.query.filter_by(nome_obra="Obra Padrão").first()
        if not obra_padrao:
            obra_padrao = Obra(
                numero_obra="0000",
                nome_obra="Obra Padrão",
                descricao="Obra padrão para alocações gerais",
                ativa=True,
                status="Em Andamento"
            )
            db.session.add(obra_padrao)
        
        db.session.commit()
        print("✅ Dados básicos criados/verificados")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar dados básicos: {e}")
        db.session.rollback()
        return False

def verificar_integridade_banco():
    """Verifica a integridade básica do banco de dados"""
    try:
        # Verificar se as tabelas principais existem
        from sqlalchemy import inspect
        insp = inspect(db.engine)
        tabelas_necessarias = ['users', 'funcionarios', 'categorias', 'fornecedores', 'obras', 'produtos', 'movimentacoes']
        tabelas_existentes = insp.get_table_names()
        
        tabelas_faltando = [t for t in tabelas_necessarias if t not in tabelas_existentes]
        if tabelas_faltando:
            print(f"⚠️  Tabelas faltando: {tabelas_faltando}")
            return False
        
        # Verificar se há pelo menos um usuário admin
        admin_count = User.query.filter_by(tipo_usuario="almoxarifado").count()
        if admin_count == 0:
            print("⚠️  Nenhum usuário admin encontrado")
            return False
        
        # Verificar se há funcionário Sistema
        funcionario_sistema = Funcionario.query.filter_by(nome="Sistema").first()
        if not funcionario_sistema:
            print("⚠️  Funcionário Sistema não encontrado")
            return False
        
        print("✅ Integridade do banco verificada")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar integridade: {e}")
        return False

def init_render_db():
    """Inicializa o banco de dados no Render com validações robustas"""
    with app.app_context():
        try:
            print("🚀 Iniciando configuração do banco de dados...")
            
            # 1. Aplicar migrações
            print("📦 Aplicando migrações...")
            upgrade()
            print("✅ Migrações aplicadas com sucesso!")
            
            # 2. Criar usuário admin
            if not criar_usuario_admin():
                print("❌ Falha ao criar usuário admin")
                return False
            
            # 3. Criar funcionário sistema
            if not criar_funcionario_sistema():
                print("❌ Falha ao criar funcionário sistema")
                return False
            
            # 4. Criar dados básicos
            if not criar_dados_basicos():
                print("❌ Falha ao criar dados básicos")
                return False
            
            # 5. Verificar integridade
            if not verificar_integridade_banco():
                print("❌ Falha na verificação de integridade")
                return False
            
            print("\n🎉 Banco de dados inicializado com sucesso!")
            print("📋 Resumo:")
            print(f"   - Usuários: {User.query.count()}")
            print(f"   - Funcionários: {Funcionario.query.count()}")
            print(f"   - Categorias: {Categoria.query.count()}")
            print(f"   - Fornecedores: {Fornecedor.query.count()}")
            print(f"   - Obras: {Obra.query.count()}")
            
            return True
            
        except Exception as e:
            print(f"💥 Erro crítico durante inicialização: {e}")
            return False

if __name__ == '__main__':
    sucesso = init_render_db()
    if not sucesso:
        sys.exit(1)
    print("\n✨ Inicialização concluída com sucesso!")

