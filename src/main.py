import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

from src.models.user import db, User
from src.models.almoxarifado import Produto, Obra, Funcionario, Movimentacao, Categoria, Fornecedor
from src.routes.user import user_bp, login_required
from src.routes.almoxarifado import almoxarifado_bp
from src.config import config


def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))
    
    # Carrega configuração baseada no ambiente
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configuração CORS para permitir acesso externo
    CORS(app)
    
    # Registra blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(almoxarifado_bp)
    
    # Inicializa banco de dados e migrate
    db.init_app(app)
    Migrate(app, db)

    # 🔹 Registra comandos customizados
    register_commands(app)

    # 🔹 Garante criação das tabelas no banco (SQLite ou Postgres)
    with app.app_context():
        try:
            db.create_all()
            from sqlalchemy import inspect
            insp = inspect(db.engine)
            print("✅ Tabelas no banco:", insp.get_table_names())
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")

    return app



def register_commands(app):
    """Registra comandos customizados no flask CLI"""

    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """Cria usuário admin master e funcionário padrão"""
        # Criar usuário admin master se não existir
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
            click.echo("✅ Usuário admin master criado: Monter / almox")

        # Criar funcionário padrão se não existir
        funcionario_padrao = Funcionario.query.filter_by(id=1).first()
        if not funcionario_padrao:
            funcionario_padrao = Funcionario(
                id=1,
                nome="Sistema",
                cargo="Operador do Sistema",
                ativo=True
            )
            db.session.add(funcionario_padrao)
            db.session.commit()
            click.echo("✅ Funcionário padrão criado: Sistema")


# Cria a aplicação
app = create_app()


# Inicialização do banco apenas se executado diretamente
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


@app.route("/")
@app.route("/<path:path>")
@login_required
def serve(path):
    # Verificar tipo de usuário
    user = User.query.get(session["user_id"])
    if user.tipo_usuario == "producao":
        return redirect("/producao")

    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, "index.html")
        else:
            return "index.html not found", 404


@app.route("/gerenciamento")
@login_required
def gerenciamento():
    return render_template("gerenciamento_obras.html")


@app.route("/locais")
@login_required
def locais():
    return render_template("gerenciamento_locais.html")
