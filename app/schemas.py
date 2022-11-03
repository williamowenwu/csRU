from pydantic import BaseModel, EmailStr


class Course(BaseModel):
    profs: list
    course_title: str
    rutgers_course_id: str
    is_elective: bool = False


class CourseResponse(BaseModel):
    course_title: str
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
