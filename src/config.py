import os
from urllib.parse import quote_plus

class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "asdf#FGSgvasgf$5$WGT"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento - usa SQLite"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

class ProductionConfig(Config):
    """Configuração para produção - usa PostgreSQL"""
    DEBUG = False

    raw_url = os.environ.get("DATABASE_URL")

    if raw_url:
        # Normaliza o prefixo para usar psycopg2
        if raw_url.startswith("postgres://"):
            raw_url = raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif raw_url.startswith("postgresql://"):
            raw_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

        SQLALCHEMY_DATABASE_URI = raw_url
    else:
        DB_HOST = os.environ.get("DB_HOST", "localhost")
        DB_PORT = os.environ.get("DB_PORT", "5432")
        DB_NAME = os.environ.get("DB_NAME", "almoxarifado")
        DB_USER = os.environ.get("DB_USER", "postgres")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

        if DB_PASSWORD:
            encoded_password = quote_plus(DB_PASSWORD)
            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:
            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Dicionário de configurações
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}



