from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..storage import models
from ..domain import schemas, validate
from ..storage.database import get_db
from ..auth import oauth2

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()

    course_models = [validate.ValidateCourse.from_db_course(model) for model in courses]
    return [course_model.dict(exclude={"id", "created_at"}) for course_model in course_models]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(course: validate.ValidateCourse, db: Session = Depends(get_db)):
    # * The ** unpacks the entire dictionary
    new_course = models.Course(**course.dict())

    db.add(new_course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course already exists"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(new_course)  # Equivalent to SQL command: RETURNING *
    return course


@router.get("/{id}")
def get_id_course(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
):
    course = db.query((models.Course)).get(id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )
    return course


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
):
    course_to_delete = db.query(models.Course).filter(models.Course.id == id)

    if not course_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )
    course_to_delete.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_course(
    id: int,
    course: schemas.Course,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):

    updated_course = db.query(models.Course).filter(models.Course.id == id)

    course_query = updated_course.first()
    if not course_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )
    updated_course.update(course.dict(), synchronize_session=False)
    db.commit()

    return updated_course.first()


@router.get("/{course_id}/professors")
def get_professors_of_course_id(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).get(course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {course_id} doesn't exist"
        )
    return course.profs


@router.post("/professor-teaching", response_model=schemas.ProfCourse)  # join tables
def link_course_with_prof(prof_course: schemas.ProfCourse, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == prof_course.course_id)
    prof = db.query(models.Professor).filter(models.Professor.id == prof_course.professor_id)

    course_query = course.first()
    prof_query = prof.first()

    if not course_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"course with id {prof_course.course_id} doesn't exist",
        )

    if not prof_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no professor with id: {prof_course.professor_id}",
        )

    # todo: need to figure out duplicate rows
    prof_course.course_id = prof_course.course_id
    new_prof_course_connection = models.course_professor(**prof_course.dict())
    db.add(new_prof_course_connection)
    db.commit()
    db.refresh(new_prof_course_connection)

    return new_prof_course_connection
