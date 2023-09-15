import datetime

from pydantic import BaseModel, EmailStr
from ..storage import models


class Course(BaseModel):
    profs: list
    course_title: str
    rutgers_course_id: str
    course_credits: int
    comments: str | None
    sections: list
    is_elective: bool = False
    created_at: datetime.datetime | None
    id: int | None

    @classmethod
    def from_db_course(cls, course: models.Course):
        return cls(
            profs=course.profs,
            sections=course.sections,
            course_title=course.course_title,
            rutgers_course_id=course.rutgers_course_id,
            course_credits=course.course_credits,
            comments=course.comments,
            is_elective=course.is_elective,
            created_at=course.created_at,
            id=course.id,
        )


class CourseResponse(BaseModel):
    rutgers_course_title: str
    rutgers_course_id: str
    is_elective: bool

    class Config:
        orm_mode = True


class Professor(BaseModel):
    name: str
    location: str


class ProfessorResponse(Professor):
    class Config:
        orm_mode = True


class ProfCourse(BaseModel):
    course_id: int
    professor_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Schema if token is generated.
class TokenData(BaseModel):
    id: str | None  # optional
