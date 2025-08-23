import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.almoxarifado import Produto, Obra, Funcionario, Movimentacao, Categoria, Fornecedor
from datetime import datetime, date
from pytz import timezone

SAO_PAULO_TZ = timezone("America/Sao_Paulo")

def populate_database(app):
    with app.app_context():
        # Limpar dados existentes
        db.drop_all()
        db.create_all()

        # Criar alguns locais de exemplo
        from src.models.almoxarifado import Local

        if Local.query.count() == 0:
            locais_exemplo = [
                Local(nome_local="Rua 1", posicao="1.1", descricao="Primeira rua do almoxarifado"),
                Local(nome_local="Rua 2", posicao="2.1", descricao="Segunda rua do almoxarifado"),
                Local(nome_local="Rua 3", posicao="3.1", descricao="Terceira rua do almoxarifado"),
                Local(nome_local="Rua 4", posicao="4.1", descricao="Quarta rua do almoxarifado"),
                Local(nome_local="Setor A", posicao="A.1-B", descricao="Setor especial para materiais frágeis"),
                Local(nome_local="Galpão 1", posicao="G1.2-3", descricao="Galpão para materiais grandes")
            ]

            for local in locais_exemplo:
                db.session.add(local)

        db.session.commit()

        # Criar categorias padrão
        categorias = [
            Categoria(nome='Curva A', descricao='Produtos de alta rotatividade e alto valor'),
            Categoria(nome='Curva B', descricao='Produtos de média rotatividade e valor médio'),
            Categoria(nome='Curva C', descricao='Produtos de baixa rotatividade e baixo valor'),
            Categoria(nome='Material Elétrico', descricao='Componentes e materiais elétricos'),
            Categoria(nome='Ferramentas', descricao='Ferramentas manuais e equipamentos'),
            Categoria(nome='Acabamento', descricao='Materiais de acabamento e pintura')
        ]

        for categoria in categorias:
            db.session.add(categoria)

        # Criar fornecedores padrão
        fornecedores = [
            Fornecedor(nome='Construtora ABC'),
            Fornecedor(nome='Materiais São José'),
            Fornecedor(nome='Elétrica Central'),
            Fornecedor(nome='Ferramentas & Cia'),
            Fornecedor(nome='Acabamentos Premium'),
            Fornecedor(nome='Distribuidora Norte')
        ]

        for fornecedor in fornecedores:
            db.session.add(fornecedor)

        # Criar funcionários
        funcionarios = [
            Funcionario(nome='João Silva', cargo='Almoxarife'),
            Funcionario(nome='Maria Santos', cargo='Auxiliar de Almoxarifado'),
            Funcionario(nome='Pedro Oliveira', cargo='Supervisor'),
            Funcionario(nome='Ana Costa', cargo='Técnico')
        ]

        for funcionario in funcionarios:
            db.session.add(funcionario)

        # Criar obras
        obras = [
            Obra(numero_obra='OB001', nome_obra='Construção Edifício Central', 
                 descricao='Construção de edifício comercial', data_inicio=date(2024, 1, 15), ativa=True),
            Obra(numero_obra='OB002', nome_obra='Reforma Shopping Norte', 
                 descricao='Reforma completa do shopping', data_inicio=date(2024, 2, 1), ativa=True),
            Obra(numero_obra='OB003', nome_obra='Ponte Rio Verde', 
                 descricao='Construção de ponte sobre o rio', data_inicio=date(2024, 3, 10), ativa=True),
            Obra(numero_obra='OB004', nome_obra='Residencial Jardins', 
                 descricao='Conjunto residencial', data_inicio=date(2024, 1, 20), ativa=False)
        ]

        for obra in obras:
            db.session.add(obra)

        # Criar produtos
        produtos = [
            Produto(codigo='P001', nome='Cimento Portland CP-II', descricao='Saco 50kg', 
                   fornecedor='Construtora ABC', categoria='Curva A', local_produto='A1-01', 
                   preco=25.50, quantidade_estoque=150),
            Produto(codigo='P002', nome='Tijolo Cerâmico 6 furos', descricao='Tijolo comum 9x14x19cm', 
                   fornecedor='Materiais São José', categoria='Curva A', local_produto='B2-05', 
                   preco=0.85, quantidade_estoque=5000),
            Produto(codigo='P003', nome='Areia Média', descricao='Metro cúbico', 
                   fornecedor='Distribuidora Norte', categoria='Curva B', local_produto='C1-01', 
                   preco=45.00, quantidade_estoque=25),
            Produto(codigo='P004', nome='Brita 1', descricao='Metro cúbico', 
                   fornecedor='Pedreira Central', categoria='Curva B', local_produto='C1-02', 
                   preco=55.00, quantidade_estoque=30),
            Produto(codigo='P005', nome='Vergalhão 10mm', descricao='Barra 12m CA-50', 
                   fornecedor='Aços Unidos', categoria='Curva A', local_produto='D1-01', 
                   preco=35.80, quantidade_estoque=200),
            Produto(codigo='P006', nome='Tinta Acrílica Branca', descricao='Lata 18L', 
                   fornecedor='Tintas Premium', categoria='Curva C', local_produto='E1-03', 
                   preco=89.90, quantidade_estoque=45),
            Produto(codigo='P007', nome='Porta de Madeira', descricao='Porta 80x210cm', 
                   fornecedor='Madeiras Nobre', categoria='Curva C', local_produto='F2-01', 
                   preco=180.00, quantidade_estoque=12),
            Produto(codigo='P008', nome='Telha Cerâmica', descricao='Telha colonial', 
                   fornecedor='Cerâmica São José', categoria='Curva B', local_produto='G1-01', 
                   preco=2.50, quantidade_estoque=800),
            Produto(codigo='P009', nome='Tubo PVC 100mm', descricao='Tubo 6m esgoto', 
                   fornecedor='Tubos Brasil', categoria='Curva B', local_produto='H1-02', 
                   preco=45.60, quantidade_estoque=60),
            Produto(codigo='P010', nome='Fio Elétrico 2.5mm', descricao='Rolo 100m', 
                   fornecedor='Cabos Elétricos', categoria='Curva C', local_produto='I1-01', 
                   preco=125.00, quantidade_estoque=25)
        ]

        for produto in produtos:
            db.session.add(produto)

        # Commit para gerar IDs
        db.session.commit()

        # Criar algumas movimentações de exemplo
        movimentacoes = [
            Movimentacao(produto_id=1, obra_id=1, funcionario_id=1, tipo_movimentacao='ALOCACAO',
                        quantidade=50, valor_unitario=25.50, valor_total=1275.00,
                        data_movimentacao=SAO_PAULO_TZ.localize(datetime(2024, 8, 15, 10, 30)),
                        observacoes='Alocação para fundação'),
            Movimentacao(produto_id=2, obra_id=1, funcionario_id=2, tipo_movimentacao='ALOCACAO',
                        quantidade=1000, valor_unitario=0.85, valor_total=850.00,
                        data_movimentacao=SAO_PAULO_TZ.localize(datetime(2024, 8, 16, 14, 15)),
                        observacoes='Tijolos para alvenaria'),
            Movimentacao(produto_id=5, obra_id=2, funcionario_id=1, tipo_movimentacao='ALOCACAO',
                        quantidade=30, valor_unitario=35.80, valor_total=1074.00,
                        data_movimentacao=SAO_PAULO_TZ.localize(datetime(2024, 8, 17, 9, 45)),
                        observacoes='Vergalhões para estrutura'),
            Movimentacao(produto_id=3, obra_id=3, funcionario_id=3, tipo_movimentacao='ALOCACAO',
                        quantidade=10, valor_unitario=45.00, valor_total=450.00,
                        data_movimentacao=SAO_PAULO_TZ.localize(datetime(2024, 8, 18, 11, 20)),
                        observacoes='Areia para concreto'),
            Movimentacao(produto_id=6, obra_id=1, funcionario_id=2, tipo_movimentacao='ALOCACAO',
                        quantidade=5, valor_unitario=89.90, valor_total=449.50,
                        data_movimentacao=SAO_PAULO_TZ.localize(datetime(2024, 8, 19, 16, 10)),
                        observacoes='Tinta para acabamento')
        ]

        for movimentacao in movimentacoes:
            db.session.add(movimentacao)
            # Atualizar estoque do produto
            produto = Produto.query.get(movimentacao.produto_id)
            if produto:
                produto.quantidade_estoque -= movimentacao.quantidade

        db.session.commit()
        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    from src.main import app
    populate_database(app)