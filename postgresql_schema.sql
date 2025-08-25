
CREATE TABLE categorias (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	descricao VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE fornecedores (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	contato VARCHAR(100), 
	telefone VARCHAR(20), 
	email VARCHAR(120), 
	PRIMARY KEY (id), 
	UNIQUE (nome)
)

;


CREATE TABLE funcionarios (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	cargo VARCHAR(100), 
	ativo BOOLEAN, 
	PRIMARY KEY (id)
)

;


CREATE TABLE movimentacoes (
	id SERIAL NOT NULL, 
	produto_id INTEGER, 
	quantidade INTEGER NOT NULL, 
	tipo_movimentacao VARCHAR(20) NOT NULL, 
	data_movimentacao TIMESTAMP WITHOUT TIME ZONE, 
	obra_id INTEGER, 
	funcionario_id INTEGER, 
	observacao VARCHAR(255), 
	PRIMARY KEY (id)
)

;


CREATE TABLE obras (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	localizacao VARCHAR(255), 
	data_inicio TIMESTAMP WITHOUT TIME ZONE, 
	data_fim TIMESTAMP WITHOUT TIME ZONE, 
	ativo BOOLEAN, 
	PRIMARY KEY (id)
)

;


CREATE TABLE produtos (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	descricao VARCHAR(255), 
	quantidade INTEGER NOT NULL, 
	unidade_medida VARCHAR(20), 
	preco_unitario VARCHAR(20), 
	categoria_id INTEGER, 
	fornecedor_id INTEGER, 
	data_cadastro TIMESTAMP WITHOUT TIME ZONE, 
	ativo BOOLEAN, 
	PRIMARY KEY (id)
)

;


CREATE TABLE users (
	id SERIAL NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	tipo_usuario VARCHAR(20) NOT NULL, 
	ativo BOOLEAN, 
	data_cadastro TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
)

;

