# Student CRUD API

A small FastAPI project that shows the same layered structure we use in ReX.
The example resource is a **Book** (create, read, update, delete).

## Run it

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try every endpoint. The SQLite database file
(`students.db`) is created automatically on first start.

## Folder structure

```
main.py            Starting point. Creates the app and registers the routers.
config.py          Settings, read from .env.
constants/         Fixed values (HTTP status codes).
database/          Database connection (engine, session, get_db).
models/            Database tables.
schemas/           Request / response shapes (validation).
repositories/      Layer 4 - runs the database queries.
services/          Layer 3 - business rules.
controllers/       Layer 2 - calls the service, handles errors, formats the response.
routes/            Layer 1 - defines the URLs only.
middlewares/       Custom errors, error handler, standard response format.
```

## How a request travels

```
Client -> routes -> controllers -> services -> repositories -> database
                                                                  |
Client <- routes <- controllers <- services <- repositories <-----+
```

Each layer only talks to the one directly below it. Routes never touch the
database; repositories never raise HTTP errors.

## Endpoints

| Method | URL                | What it does                       |
|--------|--------------------|------------------------------------|
| POST   | /api/books         | Create a book                      |
| GET    | /api/books         | List books (`page`, `limit`, `search`) |
| GET    | /api/books/{id}    | Get one book                       |
| PUT    | /api/books/{id}    | Update a book (send only changed fields) |
| DELETE | /api/books/{id}    | Delete a book                      |

## Adding a new module (e.g. Student)

Copy the five `book_*` files, rename them to `student_*`, then:
1. Edit `models/student_models.py` and import it in `database/database.py` (`init_db`).
2. Edit the schema, repository, service, controller and route.
3. Register the router in `main.py`.
