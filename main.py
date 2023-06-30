from fastapi import FastAPI
from db import models
from db.database import engine
from routers import users,posts
from fastapi.staticfiles import StaticFiles
from auth import authentication



app = FastAPI()
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)


models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')