# FastRank - FastAPI Game Rank System

This package is a ready to use rank system, Using FastAPI, PostgreSQL. It includes the 
API routes, built in utilities, database session and ORM models.

> ## Install Package

```
pip install "git+https://github.com/tech1919/fastapi-rank.git"
```


> ## Configure Environment

Configure `.env` file:
```
RANK_DATABASE_URL=postgres://username:password@host:port/database_name
```

> ## Add the router to your FastAPI app

import:
```python
from fastrank.router import rank_router
from fastapi import FastAPI
```

define the app:
```python
app = FastAPI(
    title = "API's name"
)
```

include the router:
```python
app.include_router(router = rank_router , prefix="/rank")
```



