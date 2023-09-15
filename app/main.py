from fastapi import FastAPI

from app.storage import models
from app.storage.database import engine
from app.routers import course, user, auth, professor, rmp, course_section

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(professor.router)
app.include_router(rmp.router)
app.include_router(course_section.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
