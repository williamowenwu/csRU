from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.storage import models
from app.domain import validate
from app.storage.database import get_db

router = APIRouter(prefix='/course_sections', tags=["CourseSection"])


@router.get("/{course_id}")
def get_sections_for_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.rutgers_course_id == course_id).first()
    if course:
        all_query = db.query(models.CourseSection).filter(
            models.CourseSection.rutgers_course_id == course_id
        ).all()

        courses = [validate.ValidateSections.from_db_section(query) for query in all_query]
        return [course.dict(exclude={"id", "created_at"}) for course in courses]

    raise HTTPException(
        detail="Course does not exist",
        status_code=status.HTTP_404_NOT_FOUND
    )


@router.post("/{course_id}")
def create_sections_for_course(
    course_sections: List[validate.ValidateSections],
    course_id: str,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(models.Course.rutgers_course_id == course_id).first()
    if not course:
        raise HTTPException(
            detail="Course does not exist",
            status_code=status.HTTP_404_NOT_FOUND
        )

    for section in course_sections:
        section_dict = section.dict()
        if section_dict['rutgers_course_id'] != course.rutgers_course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid section course id"
            )
        new_section = models.CourseSection(**section_dict)
        course.sections.append(new_section)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            detail="Invalid sections, duplicate sections",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(course)
    section_models = [
        validate.ValidateSections.from_db_section(course) for course in course.sections
    ]
    return [section_model.dict(exclude={"id", "created_at"}) for section_model in section_models]

# todo: for all sections or one section
# @router.put("/{course_id}")
# def update_all_sections(
#     course_sections: List[validate.ValidateSections],
#     course_id: str,
#     db: Session = Depends(get_db)
# ):
#     course_query = db.query(models.Course).filter(models.Course.rutgers_course_id == course_id)

#     course = course_query.first()
#     if course:
#         # update the model
#         course_query.update()
#         # return it

#     for section in course_sections:
#         section.dict(exclude_unset=)
#     #duplicate course

# update just 1 section of a course
@router.patch("/{course_id}")
