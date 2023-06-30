from fastapi import FastAPI
from db import models
from db.database import engine
from routers import users,posts



app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)


models.Base.metadata.create_all(engine)