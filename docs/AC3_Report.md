## AC3 - Atividade Hands-On de Quality Assurance

### 1. Identificacao do grupo

- **Grupo:** Lost Birds
- **Projeto:** User Management API
- **Integrantes:**
  - Joao Vitor de Morais Timotio - 103916
  - Eduardo Oliveira Silva - 106462
  - Gabriel Cardoso Pereira - 106415
  - Sabrina Paes Novais - 106490
  - William Cesar Silva de Carvalho - 105637

### 2. Descricao do sistema

- **Nome do sistema:** User Management API
- **Objetivo:** disponibilizar uma API REST para cadastro, consulta, atualizacao e desativacao de usuarios.
- **O que o sistema faz:** recebe requisicoes HTTP e executa operacoes de CRUD sobre a tabela `users`, aplicando validacoes de negocio para nome, e-mail e senha.
- **Como funciona:** as rotas Flask em `/users` recebem os dados, o controller delega para o service, o service valida as entradas e o repository realiza a persistencia no PostgreSQL.

### 3. Escopo dos testes

Nesta atividade foram validadas as seguintes partes do sistema:

- criacao de usuarios;
- listagem de usuarios;
- busca por usuario inexistente;
- validacao de e-mail;
- validacao de senha;
- tratamento de payload invalido;
- desativacao logica de usuario;
- atualizacao de dados do usuario.

### 4. Tipos de teste aplicados

- teste funcional;
- teste de API;
- validacao de dados;
- testes com erro proposital;
- testes automatizados em Python.

### 5. Divisao de responsabilidades

- **Integrante 1:** execucao do sistema (prototipo/API local)
- **Integrante 2:** execucao dos testes automatizados
- **Integrante 3:** documentacao
- **Integrante 4:** coleta de evidencias
- **Integrante 5:** analise de bugs e melhorias

### 6. Casos de teste

| ID | Nome | Objetivo | Entrada | Passos | Resultado esperado |
| --- | --- | --- | --- | --- | --- |
| CT-01 | Criar usuario valido | Garantir que um usuario valido seja cadastrado | `{"name":"Ana","email":"ana@email.com","password":"Senha123"}` | Enviar `POST /users/` com JSON valido | Retornar `201` com usuario criado |
| CT-02 | Listar usuarios | Garantir que a listagem da API funcione | Sem body | Enviar `GET /users/` | Retornar `200` com lista de usuarios |
| CT-03 | Buscar usuario inexistente | Validar o tratamento de id nao encontrado | `id=999` | Enviar `GET /users/999` | Retornar `404` com mensagem `Usuario nao encontrado` |
| CT-04 | Criar usuario com payload vazio | Validar erro de campos obrigatorios | `{}` | Enviar `POST /users/` sem campos | Retornar `400` com mensagem de erro |
| CT-05 | Criar usuario com e-mail invalido | Garantir validacao do formato de e-mail | `name=William`, `email=email-invalido`, `password=Senha123` | Executar chamada de cadastro | Lancar erro `Email invalido` |
| CT-06 | Criar usuario com senha fraca | Garantir validacao minima da senha | `name=William`, `email=william@email.com`, `password=12345678` | Executar chamada de cadastro | Lancar erro `Senha invalida` |

### 7. Execucao dos testes

| ID | Status | Comportamento observado | Comparacao com o esperado |
| --- | --- | --- | --- |
| CT-01 | Passou | O endpoint retornou `201` e devolveu o nome do usuario criado | Conforme esperado |
| CT-02 | Passou | O endpoint retornou `200` com um item na lista | Conforme esperado |
| CT-03 | Passou | O endpoint retornou `404` e mensagem `Usuario nao encontrado` | Conforme esperado |
| CT-04 | Passou | O endpoint retornou `400` ao receber payload vazio | Conforme esperado |
| CT-05 | Passou | O service rejeitou o e-mail invalido com `ValueError` | Conforme esperado |
| CT-06 | Passou | O service rejeitou a senha fraca com `ValueError` | Conforme esperado |

### 8. Evidencias coletadas

Arquivos gerados nesta atividade:

- `docs/AC3_Report.md` - documento consolidado da atividade;
- `docs/test_execution_evidence.txt` - evidencia textual da execucao automatizada no terminal;
- `tests/test_user_routes.py` - testes automatizados de API;
- `tests/test_user_service.py` - testes automatizados das regras de negocio;
- `app/schemas/validors.py` - validacoes implementadas;
- `app/utils/validators.py` - adaptador para uso das validacoes no service.

### 9. Testes com erro proposital

Entradas invalidas executadas:

1. **Campo vazio**
   - payload `{}` em `POST /users/`
   - comportamento: retorno `400` com erro de dados obrigatorios ausentes

2. **Tipo/formato de dado incorreto**
   - e-mail `email-invalido`
   - comportamento: rejeicao com `Email invalido`

3. **Valor invalido**
   - senha `12345678`
   - comportamento: rejeicao com `Senha invalida`

4. **Dados incompletos**
   - ausencia de `name`, `email` e `password`
   - comportamento: retorno `400`

### 10. Testes de API

#### Testes validos

1. `GET /users/` retorna `200`
2. `POST /users/` com payload valido retorna `201`

#### Testes invalidos

1. `POST /users/` com payload vazio retorna `400`
2. `GET /users/999` retorna `404`

### 11. Automacao de testes

Foram implementados 10 testes automatizados em Python, superando o minimo de 2 solicitado:

- **Arquivo:** `tests/test_user_routes.py`
  - cobre 2 testes de API validos e 2 invalidos
- **Arquivo:** `tests/test_user_service.py`
  - cobre validacao de e-mail, senha, duplicidade, atualizacao e desativacao

**Comando executado:**

```bash
python -m unittest discover -s tests -v
```

**Resultado obtido:** `Ran 10 tests ... OK`

### 12. Bugs identificados

#### Bug 1 - Modulo de validacao inexistente

- **Descricao:** o arquivo importado em `app.services.user_service` (`app.utils.validators`) nao existia no projeto.
- **Como reproduzir:** executar qualquer import do service ou iniciar a aplicacao.
- **Impacto:** a API nao sobe corretamente, impedindo o uso do sistema.
- **Sugestao de correcao:** manter um modulo de validacao reutilizavel e coberto por testes.

#### Bug 2 - Falta de tratamento para parametros invalidos na listagem

- **Descricao:** `limit` e `offset` sao convertidos diretamente com `int()` no controller.
- **Como reproduzir:** chamar `GET /users/?limit=abc`.
- **Impacto:** a aplicacao pode retornar erro interno em vez de uma resposta `400` amigavel.
- **Sugestao de correcao:** validar `limit` e `offset` antes da conversao e retornar mensagem padronizada.

### 13. Sugestoes de melhoria

#### Melhorias tecnicas

1. adicionar tratamento centralizado de erros para padronizar respostas `400`, `404` e `500`;
2. ampliar a automacao com testes de integracao ligados ao PostgreSQL real em ambiente de teste.

#### Melhoria geral

1. documentar exemplos de requisicoes e respostas no `README.md` para facilitar uso e manutencao.

### 14. Revisao final

Checklist da entrega:

- descricao do sistema: **ok**
- escopo dos testes: **ok**
- minimo de 5 casos de teste: **ok**
- execucao registrada: **ok**
- evidencias: **ok**
- testes com erro: **ok**
- testes de API: **ok**
- minimo de 2 testes automatizados: **ok**
- minimo de 2 bugs: **ok**
- melhorias propostas: **ok**
