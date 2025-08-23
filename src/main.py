import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template, session, redirect, url_for
from flask_cors import CORS
from src.models.user import db, User
from src.models.almoxarifado import Produto, Obra, Funcionario, Movimentacao, Categoria, Fornecedor
from src.routes.user import user_bp, login_required
from src.routes.almoxarifado import almoxarifado_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configuração CORS para permitir acesso externo
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(almoxarifado_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    
    # Criar usuário admin master se não existir
    admin_user = User.query.filter_by(username='Monter').first()
    if not admin_user:
        admin_user = User(
            username='Monter',
            email='admin@almoxarifado.com',
            tipo_usuario='almoxarifado',
            is_admin=True
        )
        admin_user.set_password('almox')
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário admin criado: Monter / almox")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def serve(path):
    # Verificar tipo de usuário
    user = User.query.get(session['user_id'])
    if user.tipo_usuario == 'producao':
        return redirect('/producao')
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/gerenciamento')
@login_required
def gerenciamento():
    return render_template('gerenciamento_obras.html')

@app.route('/locais')
@login_required
def locais():
    return render_template('gerenciamento_locais.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)