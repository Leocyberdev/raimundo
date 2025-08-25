"""
Correções para o arquivo src/routes/almoxarifado.py
Melhorias na validação de usuários e funcionários
"""

# Função melhorada para obter ou criar funcionário baseado no usuário logado
def obter_funcionario_usuario_logado():
    """
    Obtém ou cria funcionário baseado no usuário logado
    Retorna o ID do funcionário ou None se houver erro
    """
    from flask import session
    from src.models.user import User
    from src.models.almoxarifado import Funcionario, db
    
    try:
        user_id = session.get('user_id')
        if not user_id:
            print("⚠️  Nenhum usuário na sessão")
            return None
        
        # Buscar usuário
        user = User.query.get(user_id)
        if not user:
            print(f"⚠️  Usuário com ID {user_id} não encontrado")
            return None
        
        # Buscar funcionário existente com o nome do usuário
        funcionario = Funcionario.query.filter_by(
            nome=user.username, 
            ativo=True
        ).first()
        
        if not funcionario:
            # Criar funcionário automaticamente
            funcionario = Funcionario(
                nome=user.username,
                cargo='Almoxarifado',
                ativo=True
            )
            db.session.add(funcionario)
            db.session.flush()  # Para obter o ID sem fazer commit
            print(f"✅ Funcionário criado automaticamente: {user.username}")
        
        return funcionario.id
        
    except Exception as e:
        print(f"❌ Erro ao obter funcionário: {e}")
        return None

def obter_funcionario_sistema():
    """
    Obtém o funcionário Sistema como fallback
    Cria se não existir
    """
    from src.models.almoxarifado import Funcionario, db
    
    try:
        funcionario_sistema = Funcionario.query.filter_by(
            nome='Sistema', 
            ativo=True
        ).first()
        
        if not funcionario_sistema:
            funcionario_sistema = Funcionario(
                nome='Sistema',
                cargo='Sistema',
                ativo=True
            )
            db.session.add(funcionario_sistema)
            db.session.flush()
            print("✅ Funcionário Sistema criado como fallback")
        
        return funcionario_sistema.id
        
    except Exception as e:
        print(f"❌ Erro ao obter funcionário Sistema: {e}")
        return 1  # ID padrão como último recurso

# Substituir a lógica de alocação de produtos (linha ~400 em almoxarifado.py)
CODIGO_ALOCACAO_MELHORADO = '''
@almoxarifado_bp.route('/api/produtos/alocar', methods=['POST'])
@login_required
def alocar_produto():
    """Alocar produto em obra com validação robusta"""
    try:
        data = request.get_json()

        produto = Produto.query.get_or_404(data['produto_id'])
        obra = Obra.query.get_or_404(data['obra_id'])
        quantidade = int(data['quantidade'])

        # Validar quantidade disponível
        if produto.quantidade_estoque < quantidade:
            return jsonify({
                'error': f'Quantidade insuficiente. Disponível: {produto.quantidade_estoque}'
            }), 400

        # Obter funcionário de forma robusta
        funcionario_id = obter_funcionario_usuario_logado()
        
        # Se não conseguir obter funcionário do usuário, usar Sistema
        if not funcionario_id:
            funcionario_id = obter_funcionario_sistema()
        
        # Validar se funcionário existe
        funcionario = Funcionario.query.get(funcionario_id)
        if not funcionario:
            return jsonify({
                'error': 'Erro interno: funcionário não encontrado'
            }), 500

        # Atualizar estoque
        produto.quantidade_estoque -= quantidade

        # Registrar movimentação
        movimentacao = Movimentacao(
            produto_id=produto.id,
            obra_id=obra.id,
            funcionario_id=funcionario_id,
            tipo_movimentacao='ALOCACAO',
            quantidade=quantidade,
            valor_unitario=produto.preco,
            valor_total=produto.preco * quantidade,
            observacoes=data.get('observacoes', '')
        )

        db.session.add(movimentacao)
        db.session.commit()

        return jsonify({
            'message': 'Produto alocado com sucesso',
            'funcionario': funcionario.nome,
            'produto': produto.nome,
            'quantidade': quantidade,
            'obra': obra.nome_obra
        })

    except Exception as e:
        db.session.rollback()
        print(f"Erro na alocação: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500
'''

# Substituir a lógica de ajuste de estoque (linha ~280 em almoxarifado.py)
CODIGO_AJUSTE_MELHORADO = '''
@almoxarifado_bp.route('/api/produtos/<int:produto_id>/ajustar-estoque', methods=['POST'])
@login_required
def ajustar_estoque(produto_id):
    """Ajustar estoque de produto com validação robusta"""
    try:
        data = request.get_json()
        produto = Produto.query.get_or_404(produto_id)
        
        operacao = data.get('operacao')
        quantidade = float(data.get('quantidade', 0))
        
        if operacao not in ['adicionar', 'retirar']:
            return jsonify({'error': 'Operação inválida'}), 400
        
        if quantidade <= 0:
            return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400

        # Validar operação de retirada
        if operacao == 'retirar' and produto.quantidade_estoque < quantidade:
            return jsonify({
                'error': f'Quantidade insuficiente. Disponível: {produto.quantidade_estoque}'
            }), 400

        # Obter funcionário de forma robusta
        funcionario_id = obter_funcionario_usuario_logado()
        
        # Se não conseguir obter funcionário do usuário, usar Sistema
        if not funcionario_id:
            funcionario_id = obter_funcionario_sistema()

        # Atualizar estoque
        if operacao == 'adicionar':
            produto.quantidade_estoque += quantidade
        else:
            produto.quantidade_estoque -= quantidade

        # Registrar movimentação
        movimentacao = Movimentacao(
            produto_id=produto.id,
            funcionario_id=funcionario_id,
            tipo_movimentacao='ENTRADA' if operacao == 'adicionar' else 'SAIDA',
            quantidade=quantidade,
            valor_unitario=produto.preco,
            valor_total=produto.preco * quantidade,
            observacoes=f'Ajuste de estoque - {operacao}'
        )

        db.session.add(movimentacao)
        db.session.commit()

        return jsonify({
            'message': f'Estoque {operacao} com sucesso',
            'nova_quantidade': produto.quantidade_estoque
        })

    except Exception as e:
        db.session.rollback()
        print(f"Erro no ajuste de estoque: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500
'''

print("Arquivo de correções criado com sucesso!")
print("Para aplicar as correções:")
print("1. Adicione as funções obter_funcionario_usuario_logado() e obter_funcionario_sistema() no início do arquivo almoxarifado.py")
print("2. Substitua a função alocar_produto() pelo código melhorado")
print("3. Substitua a função ajustar_estoque() pelo código melhorado")

