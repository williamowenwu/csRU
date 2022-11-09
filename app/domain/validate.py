import pydantic


class ValidateCourse(pydantic.BaseModel):
    course_title: str
    rutgers_course_id: str
    is_elective: bool = False

    @pydantic.validator('rutgers_course_id')
    def validate_rutgers_course_id(cls, v):
        if len(v) < 1:
            raise ValueError("incorrect id")
        return v
