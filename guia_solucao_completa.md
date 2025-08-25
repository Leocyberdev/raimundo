# Guia Completo - Solução para Migração de Dados SQLite → PostgreSQL

## 🎯 Problema Identificado

Após o deploy no Render, os dados do SQLite local não foram migrados para o PostgreSQL, causando erro "usuário com id 7 não foi encontrado" durante alocações.

## 🔍 Causa Raiz

1. **Dados não migrados**: O banco PostgreSQL no Render está vazio ou com dados incompletos
2. **Referências órfãs**: O código tenta referenciar funcionários/usuários que não existem
3. **Validação inadequada**: Falta de tratamento robusto para casos onde dados não existem

## 🛠️ Soluções Implementadas

### 1. Script de Migração Automática

**Arquivo**: `script_migracao.py`

```bash
# Uso do script
python script_migracao.py ./src/database/app.db "postgresql://user:pass@host:port/db"
```

**Funcionalidades**:
- Migra todos os dados do SQLite para PostgreSQL
- Evita duplicatas
- Respeita ordem de dependências entre tabelas
- Tratamento de erros robusto

### 2. Exportação Manual de Dados

**Arquivo**: `exportar_dados_sqlite.py`

```bash
# Gerar arquivo SQL com os dados
python exportar_dados_sqlite.py ./src/database/app.db
```

**Resultado**: Arquivo `dados_exportados.sql` com todos os dados em formato SQL para importação manual.

### 3. Inicialização Melhorada do Banco

**Arquivo**: `init_render_db_melhorado.py`

**Melhorias**:
- Validação robusta de integridade
- Criação automática de dados essenciais
- Verificações de segurança
- Logs detalhados do processo

### 4. Correções no Código da Aplicação

**Arquivo**: `correcoes_almoxarifado.py`

**Principais correções**:
- Validação robusta de usuários e funcionários
- Criação automática de funcionários quando necessário
- Fallback para funcionário "Sistema"
- Tratamento de erros melhorado

## 📋 Plano de Implementação

### Opção A: Migração Automática (Recomendada)

1. **Instalar dependências no ambiente local**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Executar migração**:
   ```bash
   python script_migracao.py ./src/database/app.db "sua_url_postgresql_do_render"
   ```

3. **Substituir arquivo de inicialização**:
   - Substituir `init_render_db.py` por `init_render_db_melhorado.py`

4. **Aplicar correções no código**:
   - Implementar as correções do arquivo `correcoes_almoxarifado.py`

### Opção B: Migração Manual

1. **Gerar arquivo SQL**:
   ```bash
   python exportar_dados_sqlite.py ./src/database/app.db
   ```

2. **Conectar ao PostgreSQL do Render** e executar o arquivo `dados_exportados.sql`

3. **Aplicar melhorias** conforme Opção A (passos 3 e 4)

## 🔧 Dados Encontrados no SQLite Local

### Usuários:
- **ID 1**: Monter (admin@almoxarifado.com) - Almoxarifado
- **ID 3**: gael (leolulu842@gmail.com) - Produção  
- **ID 4**: Reginaldo (leo@gmail.com) - Almoxarifado
- **ID 5**: lucas (lucar@gmail.com) - Almoxarifado

### Funcionários:
- **ID 1**: Sistema (Operador do Sistema)
- **ID 2**: Reginaldo (Almoxarifado)

### Outros Dados:
- **3 Categorias**: Curva A, Curva B, Curva C
- **3 Fornecedores**: Schneider, Phoenix, Connectwell
- **2 Obras**: ardag (4558), CUMMINS (4561)
- **8 Produtos**: Diversos materiais elétricos
- **Múltiplas movimentações** registradas

## ⚠️ Pontos de Atenção

1. **Backup**: Sempre faça backup do banco PostgreSQL antes da migração
2. **URL do Banco**: Certifique-se de usar a URL correta do PostgreSQL do Render
3. **Permissões**: Verifique se tem permissões de escrita no banco
4. **Teste**: Teste a aplicação após a migração para garantir funcionamento

## 🚀 Próximos Passos

1. **Escolher método de migração** (automática ou manual)
2. **Executar migração dos dados**
3. **Aplicar correções no código**
4. **Fazer novo deploy no Render**
5. **Testar funcionalidades** (especialmente alocações)

## 📞 Suporte

Se encontrar problemas durante a implementação:
1. Verifique os logs de erro detalhados
2. Confirme se todas as dependências estão instaladas
3. Valide a URL de conexão com o PostgreSQL
4. Teste a conectividade com o banco antes da migração

---

**✅ Com essas soluções, o problema de "usuário não encontrado" será resolvido e o sistema funcionará corretamente no Render com PostgreSQL.**

