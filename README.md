# FastAPI + SQLModel server for zebra
A REST API with FastAPI and SQLModel.

## How to run the project
- Install with poetry
```
poetry install
```

- Enter a poetry shell
```
poetry shell
```

- Create the database
```
python create_db.py

```

- Finally run the project
```
uvicorn main:app
```
