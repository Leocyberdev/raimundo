-- Dados exportados do SQLite
-- Gerado automaticamente

-- Dados da tabela users
INSERT INTO users (id, username, email, password_hash, tipo_usuario, ativo, data_cadastro) VALUES (1, 'Monter', 'admin@almoxarifado.com', 'scrypt:32768:8:1$sFWAQrMKwcWKqRzl$bd2665f43c50cbe2769a9bb31cc505f8425f5115535c47cc97e749ad78af607ace1301637cc2afe1dd21e0af5fa2c473d5c111362a02b95d66ff3b11769bd116', 'almoxarifado', 1, '2025-08-23 16:23:31.301681');
INSERT INTO users (id, username, email, password_hash, tipo_usuario, ativo, data_cadastro) VALUES (3, 'gael', 'leolulu842@gmail.com', 'scrypt:32768:8:1$xG7Eux9diiUOttJu$900d52e2784f770e9c961358a68ca4c972c88cfa198d3390d926ae18b23320477d93fd003db8379ee63776007434855be4b0325a090ad335f19ce25800a7d628', 'producao', 1, '2025-08-23 16:36:43.374024');
INSERT INTO users (id, username, email, password_hash, tipo_usuario, ativo, data_cadastro) VALUES (4, 'Reginaldo', 'leo@gmail.com', 'scrypt:32768:8:1$Oa0z87VrM3fvpGUE$3d80a1c9c48e2d22a6798e7ce965d7036f47b43bfedb09d2517e7f03d8432c92d56ff1b0d4bc704dca53c2fd3b3f0931cd2a9a8d424cbcfb4de66237cc8344a7', 'almoxarifado', 1, '2025-08-24 14:18:56.234425');
INSERT INTO users (id, username, email, password_hash, tipo_usuario, ativo, data_cadastro) VALUES (5, 'lucas', 'lucar@gmail.com', 'scrypt:32768:8:1$roUNv1vlD0fzyQkn$692babcbde238ba594c2775c1aeacca8566610fabf0605259bd74736349de182330a79e610b966a0a9fb6b3f067a4c116fa7bdcb051a1e21a54f532b57a94aaf', 'almoxarifado', 1, '2025-08-24 12:03:24.243719');

-- Dados da tabela funcionarios
INSERT INTO funcionarios (id, nome, cargo, ativo) VALUES (1, 'Sistema', 'Operador do Sistema', 1);
INSERT INTO funcionarios (id, nome, cargo, ativo) VALUES (2, 'Reginaldo', 'Almoxarifado', 1);

-- Dados da tabela categorias
INSERT INTO categorias (id, nome, descricao, ativa, data_criacao) VALUES (1, 'Curva A', 'Itens mais saidos', 1, '2025-08-23 09:15:03.868269');
INSERT INTO categorias (id, nome, descricao, ativa, data_criacao) VALUES (2, 'Curva B', 'Itens com Media saida', 1, '2025-08-23 09:16:03.170065');
INSERT INTO categorias (id, nome, descricao, ativa, data_criacao) VALUES (3, 'Curca C', 'Itens com pouca saida', 1, '2025-08-23 09:16:27.250404');

-- Dados da tabela fornecedores
INSERT INTO fornecedores (id, nome, ativo, data_criacao) VALUES (1, 'Schnneider', 1, '2025-08-23 09:17:03.227536');
INSERT INTO fornecedores (id, nome, ativo, data_criacao) VALUES (2, 'Phoenix', 1, '2025-08-23 09:17:11.202521');
INSERT INTO fornecedores (id, nome, ativo, data_criacao) VALUES (3, 'Connectwell', 1, '2025-08-23 09:17:20.297090');

-- Dados da tabela obras
INSERT INTO obras (id, numero_obra, nome_obra, descricao, data_inicio, data_fim, ativa, status, data_entrega) VALUES (1, '4558', 'ardag', 'obra ardag mt200', '2025-08-23', '2025-08-29', 1, 'Em Andamento', NULL);
INSERT INTO obras (id, numero_obra, nome_obra, descricao, data_inicio, data_fim, ativa, status, data_entrega) VALUES (2, '4561', 'CUMMINS', 'BT  200', '2025-08-23', '2025-08-27', 1, 'Pausada', NULL);

-- Dados da tabela locais
INSERT INTO locais (id, nome_local, posicao, descricao, ativo, data_criacao) VALUES (1, 'Rua 4', '04.01.101', '04.01. cx 101', 1, '2025-08-23 15:09:10.340110');
INSERT INTO locais (id, nome_local, posicao, descricao, ativo, data_criacao) VALUES (2, 'Rua 3', '03.01.103', '03.01. cx 103', 1, '2025-08-23 21:06:00.516954');

-- Dados da tabela produtos
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (1, '1415', 'minidisj 50 a 2p', 'minidisj 50 a Bipolar', 'Connectwell', 'Curva A', '04.01.101', 15.0, 2.0, '2025-08-23 12:11:37.168000', 1, 'unidade');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (2, '2523', 'minidisj 40 a 3p', 'minidisj 40a tripolar', 'Phoenix', 'Curca C', '04.03.102', 16.0, 8.0, '2025-08-23 12:13:36.633309', 1, 'unidade');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (3, '8545', 'termostato', 'termostato 60 graul', 'Connectwell', 'Curva A', '', 30.0, 5.0, '2025-08-23 13:38:01.732733', 0, 'unidade');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (4, '8952', 'para raio', 'para raio 220v', 'Schnneider', 'Curca C', 'Rua 4 - 04.01.101', 12.0, 8.0, '2025-08-23 13:54:13.586325', 0, 'unidade');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (5, 'teste editar', 'teste do editar', 'ajsfhuja', 'Connectwell', 'Curca C', 'Rua 4 - 04.01.101', 12.0, 6.0, '2025-08-23 14:10:55.404326', 0, 'unidade');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (6, '8965', 'cabo 6mm verde', 'cabo 6 mm verde 1kv', 'Connectwell', 'Curva A', 'Rua 4 - 04.01.101', 50.0, 50.0, '2025-08-23 16:52:50.812290', 1, 'metros');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (7, '8523', 'cabo 1 kv preto 6 mm', 'cabo preto 1 kv 6 mm', 'Schnneider', 'Curca C', 'Rua 4 - 04.01.101', 50.0, 70.0, '2025-08-23 17:32:05.821378', 1, 'metros');
INSERT INTO produtos (id, codigo, nome, descricao, fornecedor, categoria, local_produto, preco, quantidade_estoque, data_cadastro, ativo, unidade_medida) VALUES (8, '6541', 'parafuso m8 x 35', 'parafuso sextavado m8 x 35', 'Connectwell', 'Curva A', 'Rua 4 - 04.01.101', 10.0, 8.700000000000001, '2025-08-23 17:42:17.433773', 1, 'cento');

-- Dados da tabela movimentacoes
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (1, 1, 2, 1, 'ALOCACAO', 6.0, 15.0, 90.0, '2025-08-23 16:38:00.896536', 'adicionei 6 do obsoleto');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (2, 2, 1, 1, 'ALOCACAO', 3.0, 16.0, 48.0, '2025-08-23 16:45:00.247241', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (3, 1, NULL, 1, 'ENTRADA', 6.0, 15.0, 90.0, '2025-08-23 17:20:28.572286', 'Ajuste de estoque - adicionar');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (4, 2, NULL, 1, 'SAIDA', 5.0, 16.0, 80.0, '2025-08-23 17:20:41.650660', 'Ajuste de estoque - retirar');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (5, 6, NULL, 1, 'SAIDA', 10.0, 50.0, 500.0, '2025-08-23 17:21:01.040011', 'Ajuste de estoque - retirar');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (6, 8, 2, 1, 'ALOCACAO', 1.0, 10.0, 10.0, '2025-08-23 17:43:27.086662', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (7, 7, 2, 1, 'ALOCACAO', 50.0, 50.0, 2500.0, '2025-08-23 17:44:21.227665', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (8, 2, 1, 1, 'ALOCACAO', 4.0, 16.0, 64.0, '2025-08-23 17:49:06.883988', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (9, 6, 2, 1, 'ALOCACAO', 40.0, 50.0, 2000.0, '2025-08-23 18:22:33.748693', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (10, 7, 2, 1, 'ALOCACAO', 30.0, 50.0, 1500.0, '2025-08-23 22:08:54.649009', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (11, 8, 1, 1, 'ALOCACAO', 0.2, 10.0, 2.0, '2025-08-23 23:26:53.017191', 'Atendimento de requisição #3 - ');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (12, 8, 1, 1, 'ALOCACAO', 0.1, 10.0, 1.0, '2025-08-23 23:29:12.478350', 'Atendimento de requisição #2 - ');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (13, 7, 2, 1, 'ALOCACAO', 50.0, 50.0, 2500.0, '2025-08-23 23:29:26.174334', 'Atendimento de requisição #1 - ');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (14, 1, 2, 1, 'ALOCACAO', 3.0, 15.0, 45.0, '2025-08-24 00:16:42.133069', 'Atendimento de requisição #4 - ');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (15, 1, 1, 1, 'ALOCACAO', 2.0, 15.0, 30.0, '2025-08-24 11:25:29.947615', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (16, 1, 2, 1, 'ALOCACAO', 2.0, 15.0, 30.0, '2025-08-24 11:32:52.076495', '');
INSERT INTO movimentacoes (id, produto_id, obra_id, funcionario_id, tipo_movimentacao, quantidade, valor_unitario, valor_total, data_movimentacao, observacoes) VALUES (17, 1, 2, 2, 'ALOCACAO', 1.0, 15.0, 15.0, '2025-08-24 11:43:42.845388', '');

-- Dados da tabela requisicoes
INSERT INTO requisicoes (id, produto_id, obra_id, usuario_id, quantidade_solicitada, quantidade_atendida, status, data_requisicao, data_atendimento, observacoes, observacoes_atendimento, atendido_por) VALUES (1, 7, 2, 3, 50.0, 50.0, 'ATENDIDA', '2025-08-23 22:24:41.100585', '2025-08-23 23:29:26.173141', 'entrega para o cazão o cabo', '', 1);
INSERT INTO requisicoes (id, produto_id, obra_id, usuario_id, quantidade_solicitada, quantidade_atendida, status, data_requisicao, data_atendimento, observacoes, observacoes_atendimento, atendido_por) VALUES (2, 8, 1, 3, 0.1, 0.1, 'ATENDIDA', '2025-08-23 23:24:29.699933', '2025-08-23 23:29:12.477422', 'teste', '', 1);
INSERT INTO requisicoes (id, produto_id, obra_id, usuario_id, quantidade_solicitada, quantidade_atendida, status, data_requisicao, data_atendimento, observacoes, observacoes_atendimento, atendido_por) VALUES (3, 8, 1, 3, 0.2, 0.2, 'ATENDIDA', '2025-08-23 23:25:19.718689', '2025-08-23 23:26:53.014901', 'dfh', '', 1);
INSERT INTO requisicoes (id, produto_id, obra_id, usuario_id, quantidade_solicitada, quantidade_atendida, status, data_requisicao, data_atendimento, observacoes, observacoes_atendimento, atendido_por) VALUES (4, 1, 2, 3, 3.0, 3.0, 'ATENDIDA', '2025-08-24 00:16:06.800058', '2025-08-24 00:16:42.130052', '', '', 1);

