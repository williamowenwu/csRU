from fastapi import FastAPI
from app.routers import professor

from . import models
from .database import engine
from .routers import course, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(professor.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
