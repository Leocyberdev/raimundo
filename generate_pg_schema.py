from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime
from sqlalchemy.schema import CreateTable
from src.models.user import User
from src.models.almoxarifado import Produto, Obra, Funcionario, Movimentacao, Categoria, Fornecedor

# Crie um objeto MetaData
metadata = MetaData()

# Associe as tabelas aos modelos existentes
# User.__table__.to_metadata(metadata)
# Produto.__table__.to_metadata(metadata)
# Obra.__table__.to_metadata(metadata)
# Funcionario.__table__.to_metadata(metadata)
# Movimentacao.__table__.to_metadata(metadata)
# Categoria.__table__.to_metadata(metadata)
# Fornecedor.__table__.to_metadata(metadata)

# Para cada modelo, crie uma representação de tabela e adicione ao metadata
# Isso é necessário porque o SQLAlchemy não expõe diretamente a tabela via __table__ para CreateTable

# User table
Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(80), unique=True, nullable=False),
    Column('email', String(120), unique=True, nullable=False),
    Column('password_hash', String(255), nullable=False),
    Column('tipo_usuario', String(20), nullable=False, default='almoxarifado'),
    Column('ativo', Boolean, default=True),
    Column('data_cadastro', DateTime),
)

# Produto table
Table(
    'produtos',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(100), nullable=False),
    Column('descricao', String(255)),
    Column('quantidade', Integer, nullable=False),
    Column('unidade_medida', String(20)),
    Column('preco_unitario', String(20)),
    Column('categoria_id', Integer),
    Column('fornecedor_id', Integer),
    Column('data_cadastro', DateTime),
    Column('ativo', Boolean, default=True),
)

# Obra table
Table(
    'obras',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(100), nullable=False),
    Column('localizacao', String(255)),
    Column('data_inicio', DateTime),
    Column('data_fim', DateTime),
    Column('ativo', Boolean, default=True),
)

# Funcionario table
Table(
    'funcionarios',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(100), nullable=False),
    Column('cargo', String(100)),
    Column('ativo', Boolean, default=True),
)

# Movimentacao table
Table(
    'movimentacoes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('produto_id', Integer),
    Column('quantidade', Integer, nullable=False),
    Column('tipo_movimentacao', String(20), nullable=False), # 'entrada' ou 'saida'
    Column('data_movimentacao', DateTime),
    Column('obra_id', Integer),
    Column('funcionario_id', Integer),
    Column('observacao', String(255)),
)

# Categoria table
Table(
    'categorias',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(100), unique=True, nullable=False),
    Column('descricao', String(255)),
)

# Fornecedor table
Table(
    'fornecedores',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(100), unique=True, nullable=False),
    Column('contato', String(100)),
    Column('telefone', String(20)),
    Column('email', String(120)),
)


# Crie um motor de banco de dados PostgreSQL (apenas para gerar o dialeto SQL)
engine = create_engine("postgresql://user:password@host:5432/dbname")

# Gere o DDL para cada tabela
with open("postgresql_schema.sql", "w") as f:
    for table in metadata.sorted_tables:
        f.write(str(CreateTable(table).compile(engine)) + ";\n\n")

print("Esquema PostgreSQL gerado em postgresql_schema.sql")


