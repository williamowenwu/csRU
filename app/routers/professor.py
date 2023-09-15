from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, exc
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from app.storage import models
from app.storage.database import get_db
from app.domain import validate

router = APIRouter(prefix="/professors", tags=["Professors"])


@router.get("/")
def get_all_professors(db: Session = Depends(get_db)):
    all_professors = db.query(models.Professor).all()

    prof_models = [
        validate.ValidateProfessor.from_db_prof(prof_model) for prof_model in all_professors
    ]
    return [prof.dict(exclude={"id", "created_at", "courses"}) for prof in prof_models]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_professor(professor: validate.ValidateProfessor, db: Session = Depends(get_db)):
    prof_dict = professor.dict()
    courses = prof_dict.pop('courses')
    new_prof = models.Professor(**prof_dict)

    for course_name in courses:
        course_model = db.query(models.Course).filter(
            # todo: replace this with course id once it is finished
            models.Course.rutgers_course_title == course_name
        )
        course_to_add = course_model.first()
        new_prof.crs.append(course_to_add)
    db.add(new_prof)
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Professor already exists"
        )
    except exc.FlushError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Courses must be valid"
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(new_prof)
    return professor


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(id: int, db: Session = Depends(get_db)):
    prof_to_delete = db.query(models.Professor).filter(models.Professor.id == id)

    if not prof_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found")
    prof_to_delete.delete(synchronize_session=False)
    db.commit()


@router.get("/{id}/courses")
def get_all_courses_for_professor(id: int, db: Session = Depends(get_db)):
    prof = db.query(models.Professor).get(id)
    if not prof:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found")

    course_models = [validate.ValidateCourse.from_db_course(course) for course in prof.crs]
    return [course.dict(exclude={'created_at', 'id'}) for course in course_models]

# @router.put("/{id}",
# status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ProfessorResponse)
# def update_with_put_professor(prof = schemas.Professor, db: Session = Depends(get_db)):
#     # print(prof.name)
#     print("**************************************************")
#     print(prof.location)
#     prof_to_update = db.query(models.Professor).filter(models.Professor.id == id)

#     # prof_query = prof_to_update.first()
#     # if not prof_query:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail="Professor not found")
#     print(prof.dict())
#     prof_to_update.update()
#     prof_to_update.update(prof.dict(),synchronize_session=False)
#     db.commit()

#     return prof_to_update.first()

# # #todo: geting a professor by course is a little difficult
