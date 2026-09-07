# TodoAuthApi

API REST de gerenciamento de tarefas com autenticação de usuários, feita em FastAPI.

## Tecnologias

Python, FastAPI, SQLAlchemy, SQLite, JWT, pwdlib

## Instalação

````pip install -r requirements.txt```

# Rodar a API
```uvicorn main:app --reload```

Documentação da API: http://127.0.0.1:8000/docs

## Endpoints

- `POST /register` — cadastra um novo usuário
- `POST /login` — autentica e retorna um token JWT
- `POST /tasks` — cria uma tarefa
- `GET /tasks` — lista as tarefas do usuário logado
- `PUT /tasks/{task_id}` — edita uma tarefa
- `DELETE /tasks/{task_id}` — remove uma tarefa
```
