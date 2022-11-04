from fastapi import FastAPI

from .storage import models
from .storage.database import engine
from .routers import course, user, auth, professor

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(professor.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
