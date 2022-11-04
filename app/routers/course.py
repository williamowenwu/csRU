from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..storage import models
from ..domain import schemas
from ..storage.database import get_db
from ..auth import oauth2

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    # courses = cursor.execute("""
    #                SELECT * FROM courses
    #             """).fetchall()
    # return courses
    courses = db.query(models.Course).all()
    course_models = [schemas.Course.from_db_course(model) for model in courses]
    return [course_model.dict(exclude={"id", "created_at"}) for course_model in course_models]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CourseResponse)
def create_course(course: schemas.Course, db: Session = Depends(get_db)):
    # cursor.execute("""
    #                 INSERT INTO courses
    #                 (course_title,course_id,is_elective)
    #                 VALUES(%s,%s,%s)
    #                 RETURNING *
    #                 """,
    #                 (course.course_title,course.course_id,course.is_elective))
    # new_course = cursor.fetchone()
    # conn.commit()
    new_course = course.dict()
    profs = new_course.pop("profs")
    print(profs)
    # * The ** unpacks the entire dictionary
    new_course = models.Course(**new_course)
    print(new_course)
    db.add(new_course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="course already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(new_course)  # Equivalent to SQL command: RETURNING *
    return new_course


@router.get("/{id}")
def get_id_course(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
):
    # cursor.execute("""
    #                 SELECT * FROM courses
    #                 WHERE id = %s
    #             """,[str(id)])
    # course = cursor.fetchone()
    course = db.query((models.Course)).filter(models.Course.id == id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )
    return course


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
):
    # cursor.execute("""
    #                DELETE FROM courses
    #                WHERE id = %s
    #                RETURNING *
    #             """,[str(id)])
    # deleted_course = cursor.fetchone()
    # conn.commit()
    deleted_course = db.query(models.Course).filter(models.Course.id == id)

    if deleted_course.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {id} is not found"
        )

    deleted_course.delete(synchronize_session=False)
    db.commit()

    return deleted_course


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_course(
    id: int,
    course: schemas.Course,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    #     cursor.execute("""
    #                    UPDATE courses SET
    #                    course_title = %s,
    #                    course_id = %s,
    #                    is_elective = %s
    #                    WHERE id = %s
    #                    RETURNING *""",
    #                    (course.course_title,course.course_id,course.is_elective,str(id))
    #                 )
    #     updated_course = cursor.fetchone()
    #     conn.commit()
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
    course = db.query(models.Course).filter(models.Course.id == course_id)

    course_query = course.first()
    if not course_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {course_id} doesn't exist"
        )

    profs = db.query(models.course_professor).filter(models.course_professor.course_id == course_id)

    all_profs_for_course = profs.all()
    if not all_profs_for_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There are no professors for course {course_id}",
        )
    return all_profs_for_course


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
