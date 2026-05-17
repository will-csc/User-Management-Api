# User Management API

API REST simples para gerenciamento de usuários, com persistência em PostgreSQL e endpoints de CRUD.

## Stack

- Python + Flask
- PostgreSQL

## Estrutura

```
user-management-api/
├── app/
│   ├── __init__.py
│   ├── config/
│   │   └── database.py
│   ├── controllers/
│   │   └── user_controller.py
│   ├── repositories/
│   │   └── user_repository.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── services/
│   │   └── user_service.py
│   └── utils/
│       └── security.py
├── docs/
│   └── schema.sql
├── .env
├── run.py
└── requirements.txt
```

## Variáveis de ambiente (.env)

O projeto lê variáveis do ambiente e, se existir, também carrega o arquivo `.env` na raiz.

- DB_HOST (default: localhost)
- DB_PORT (default: 5432)
- DB_NAME
- DB_USER
- DB_PASSWORD
- SECRET_KEY
- ACCESS_TOKEN_EXPIRES_IN (default: 3600)

## Banco de dados

O schema está em [schema.sql](file:///c:/Users/WILLIAM/Documents/User-Management-Api/docs/schema.sql) e cria a tabela `users`.

## Como rodar (local)

1. Crie o banco no PostgreSQL e configure o `.env`
2. Execute o schema `docs/schema.sql` no banco
3. Instale as dependências do `requirements.txt`
4. Rode a aplicação:

```bash
python run.py
```

## Endpoints

Base URL: `/users`

- `GET /users/` lista usuários (query params: `limit`, `offset`)
- `POST /users/` cria usuário
  - Body:
    - `name` (string)
    - `email` (string)
    - `password` (string, mínimo 8 caracteres)
- `GET /users/<id>` busca usuário por id
- `PUT /users/<id>` atualiza usuário (campos opcionais)
  - Body (opcionais): `name`, `email`, `password`, `is_active`
- `DELETE /users/<id>` desativa (soft delete)

## Time

- João Vitor de Morais Timotio — 103916
- Eduardo Oliveira Silva — 106462
- Gabriel Cardoso Pereira — 106415
- Sabrina Paes Novais — 106490
- William Cesar Silva de Carvalho — 105637

Grupo: Lost Birds

