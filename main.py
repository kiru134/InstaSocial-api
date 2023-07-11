import uvicorn
from fastapi import FastAPI
from db import models
from db.database import engine
from routers import users,posts,comments
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(comments.router)
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)


models.Base.metadata.create_all(engine)

origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002',
  'https://instagram-clone-gs8p.onrender.com'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

app.mount('/images', StaticFiles(directory='images'), name='images')

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)