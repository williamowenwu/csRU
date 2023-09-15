from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from app.storage import models
from app.domain import validate
from app.storage.database import get_db
# from app.auth import oauth2

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def get_all_courses(db: Session = Depends(get_db), course_id: str | None = None):
    if course_id:
        return db.query(models.Course).filter(models.Course.rutgers_course_id == course_id).first()
    courses = db.query(models.Course).all()

    course_models = [validate.ValidateCourse.from_db_course(model) for model in courses]
    return [course_model.dict(exclude={"id", "created_at"}) for course_model in course_models]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(course: validate.ValidateCourse, db: Session = Depends(get_db)):
    course_dict = course.dict()
    # * The ** unpacks the entire dictionary
    new_course = models.Course(**course_dict)
    existing_course_id = db.query(models.Course).filter(
        models.Course.rutgers_course_id == course.rutgers_course_id
    ).first()
    existing_course_title = db.query(models.Course).filter(
        models.Course.rutgers_course_title == course.rutgers_course_title
    ).first()

    if existing_course_id or existing_course_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course already exists"
        )

    db.add(new_course)
    try:
        db.commit()
    except ValidationError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect body types"
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid section information"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(new_course)  # Equivalent to SQL command: RETURNING *
    return course


# id: str, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
@router.get("/{id}")
def get_id_course(
    id: str, db: Session = Depends(get_db),  # todo: add oauth back
):
    course = db.query((models.Course)).filter(models.Course.rutgers_course_id == id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )

    return validate.ValidateCourse.from_db_course(course)


# id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    id: str, db: Session = Depends(get_db),
):
    course_query = db.query(models.Course).filter(models.Course.rutgers_course_id == id)

    if not course_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )
    course_query.delete(synchronize_session=False)
    db.commit()


@router.put("/", status_code=status.HTTP_202_ACCEPTED)
def update_course(
    course: validate.ValidateCourse,
    db: Session = Depends(get_db),
    # user_id: int = Depends(oauth2.get_current_user),
    id: int | None = None,
):
    course_to_update = (db.query(models.Course).filter(models.Course.rutgers_course_id == id)) if id else (
        db.query(models.Course).filter(models.Course.rutgers_course_id == course.rutgers_course_id)
    )

    course_query = course_to_update.first()
    if not course_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"course with id {course.rutgers_course_id} is not found"
        )

    course_dict = course.dict()
    course_to_update.update(dict(course_dict), synchronize_session=False)

    # # Update sections
    # course_query.sections.clear()  # Clear existing sections

    # for section in course.sections:
    #     if section.rutgers_course_id != course.rutgers_course_id:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Wrong section for course"
    #         )
    #     section_dict = section.dict()
    #     new_section = models.CourseSection(**section_dict)
    #     course_query.sections.append(new_section)
    # course_to_update.update(course_dict, synchronize_session=False)  # Update remaining attributes

    # try:
    #     db.commit()
    # except IntegrityError as e:
    #     db.rollback()
    #     print(e)
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="course already exists"
    #     )
    return course


@router.get("/{course_id}/professors")
def get_professors_of_course_id(course_id: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.rutgers_course_id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {course_id} doesn't exist"
        )

    try:
        return course.profs
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='class does not yet have professors'
        )
