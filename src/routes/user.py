
from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from src.models.user import User, db
from functools import wraps

user_bp = Blueprint('user', __name__)

# Decorator para verificar autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator para verificar se é admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'error': 'Acesso negado'}), 403
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/login')
def login():
    """Página de login"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.tipo_usuario == 'almoxarifado':
            return redirect('/')
        elif user and user.tipo_usuario == 'producao':
            return redirect('/producao')
    return render_template('login.html')

@user_bp.route('/api/login', methods=['POST'])
def login_post():
    """Processar login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, ativo=True).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['tipo_usuario'] = user.tipo_usuario
            
            redirect_url = '/' if user.tipo_usuario == 'almoxarifado' else '/producao'
            
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'redirect': redirect_url,
                'user': user.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Usuário ou senha incorretos'
            }), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return redirect(url_for('user.login'))

@user_bp.route('/producao')
@login_required
def producao_dashboard():
    """Dashboard da produção"""
    user = User.query.get(session['user_id'])
    if user.tipo_usuario != 'producao':
        return redirect('/')
    return render_template('producao_dashboard.html')

@user_bp.route('/gerenciamento-usuarios')
@admin_required
def gerenciamento_usuarios():
    """Página de gerenciamento de usuários"""
    return render_template('gerenciamento_usuarios.html')

# APIs para usuários
@user_bp.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    try:
        data = request.json
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Usuário já existe'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já existe'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            tipo_usuario=data.get('tipo_usuario', 'almoxarifado')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.tipo_usuario = data.get('tipo_usuario', user.tipo_usuario)
        user.ativo = data.get('ativo', user.ativo)
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        return jsonify(user.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user.ativo = False
        db.session.commit()
        return jsonify({'message': 'Usuário desativado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
