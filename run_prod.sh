#!/bin/bash

# Script para executar a aplicação em modo de produção

echo "=== Sistema de Almoxarifado - Modo Produção ==="
echo "Ambiente: Produção (PostgreSQL)"

# Define o ambiente de produção
export FLASK_ENV=production

# Verifica se a variável de ambiente DATABASE_URL está definida
if [ -z "$DATABASE_URL" ]; then
    echo "ERRO: Variável de ambiente DATABASE_URL não configurada!"
    echo "Configure: DATABASE_URL"
    exit 1
fi

# Inicializa o banco de dados se necessário
echo "Inicializando banco de dados..."
cd src && python init_db.py
cd ..

# Executa a aplicação com Gunicorn
echo "Iniciando aplicação com Gunicorn..."
echo "Configuração:"
echo "- DATABASE_URL: $DATABASE_URL"
echo "- Porta: ${PORT:-5000}"
echo "=" * 50

gunicorn -c gunicorn.conf.py src.main:app



