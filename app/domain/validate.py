import pydantic
from fastapi import HTTPException, status
from app.storage import models


class ValidateSections(pydantic.BaseModel):
    rutgers_course_id: str
    section_number: int
    exam_code: str
    meeting_time: str
    section_comments: str | None

    @classmethod
    def from_db_section(cls, course_section: models.CourseSection):
        return cls(
            id=course_section.id,
            section_comments=course_section.section_comments,
            meeting_time=course_section.meeting_time,
            exam_code=course_section.exam_code,
            section_number=course_section.section_number,
            rutgers_course_id=course_section.rutgers_course_id,
            created_at=course_section.created_at
        )


class ValidateCourse(pydantic.BaseModel):
    rutgers_course_title: str
    rutgers_course_id: str
    course_credits: int
    is_elective: bool = False
    comments: str | None

    @classmethod
    def from_db_course(cls, course: models.Course):
        """
        iterates over sections in course and creates dictionaries
        the k:v is a dictionary compre. that loops over key-value pairs and doesn't include
        '_sa_instance_state', as it is a SQLalchemy specific variable that is added
        """
        # sections = [
        #     {k: v for k, v in section.__dict__.items() if k != '_sa_instance_state'}
        #     for section in course.sections
        # ]

        return cls(
            id=models.Course.id,
            rutgers_course_title=course.rutgers_course_title,
            rutgers_course_id=course.rutgers_course_id,
            course_credits=course.course_credits,
            # sections=sections,
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

    # @pydantic.validator('course_credits')
    # def validate_course_credits(cls, v):
    #     if v <= 0 or v > 6:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #             detail="Invalid credit amount"
    #         )


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
        if campus.title() not in [
            "Busch", "Livingston", "Cook/Doug", "Cook", "Doug", "College Ave", "C/D"
        ]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Not a valid campus"
            )
            # ? Why do you need to return???
        return campus


class ValidateRMP(pydantic.BaseModel):
    date: str
    student_reviews: str
    prof_quality: int
    prof_difficulty: int
    rutgers_course_title: str
    grade_received: str | None = None
    textbook: bool | None = None
    would_take_again: bool | None = None
    attendance: bool | None = None

    @pydantic.validator('prof_quality')
    def validate_quality(cls, v):
        if not v >= 0 and v <= 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Quality must be between 1 and 5"
            )
        return v

    @pydantic.validator('prof_difficulty')
    def validate_difficulty(cls, v):
        if not v >= 0 and v <= 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Difficulty must be between 1 and 5"
            )
        return v
