import pydantic
from fastapi import HTTPException, status
from app.storage import models


class ValidateCourse(pydantic.BaseModel):
    rutgers_course_title: str
    rutgers_course_id: str
    is_elective: bool = False

    @classmethod
    def from_db_course(cls, course: models.Course):
        return cls(
            id=models.Course.id,
            rutgers_course_title=course.rutgers_course_title,
            rutgers_course_id=course.rutgers_course_id,
            is_elective=course.is_elective,
            created_at=course.created_at,
            profs=course.profs
        )

    @pydantic.validator('rutgers_course_id')
    def validate_rutgers_course_id(cls, v):
        if len(v) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="course id not valid"
            )
        return v


class ValidateProfessor(pydantic.BaseModel):
    first_name: str
    last_name: str
    university: str
    email: pydantic.EmailStr
    campus: str
    classroom: str
    courses: list

    @classmethod
    def from_db_prof(cls, prof: models.Professor):
        return cls(
            first_name=prof.first_name,
            last_name=prof.last_name,
            university=prof.university,
            email=prof.email,
            campus=prof.campus,
            classroom=prof.classroom,
            courses=prof.crs
        )

    @pydantic.validator('campus')
    def validate_campus(cls, campus):
        if campus.title() not in ["Busch", "Livingston", "Cook/Doug", "Cook", "Doug", "College Ave"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Not a valid campus"
            )
            # ? Why do you need to return???
        return campus
