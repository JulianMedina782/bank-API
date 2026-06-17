# Bank API

API bancaria REST construida con Python, FastAPI y PostgreSQL.

## Tecnologías
- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (python-jose)
- bcrypt
- Pydantic

## Endpoints

### Usuarios
- `POST /users/register` — registrar usuario
- `POST /users/login` — login y obtener token JWT
- `GET /users/me` — datos del usuario autenticado

### Cuentas
- `POST /accounts/` — crear cuenta bancaria
- `GET /accounts/me` — listar cuentas del usuario

### Transacciones
- `POST /transactions/deposit` — depositar dinero
- `POST /transactions/withdraw` — retirar dinero
- `POST /transactions/transfer` — transferir entre cuentas
- `GET /transactions/history/{account_id}` — historial

## Cómo ejecutar
```bash
uvicorn app.main:app --reload
```

## Documentación
Disponible en `http://127.0.0.1:8000/docs`