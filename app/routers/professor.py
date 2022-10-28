from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas

router = APIRouter(
    prefix="/professors",
    tags=['Professors']
)

@router.get("/")
def get_all_professors(db: Session = Depends(get_db)):
    all_professors = db.query(models.Professor).all()
    return all_professors

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProfessorResponse)
def create_professor(professor : schemas.Professor, db: Session = Depends(get_db)):
    professor.name = professor.name.title()
    if db.query(models.Professor).filter(models.Professor.name == professor.name).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Professor {professor.name} already exists")
    
    new_professor = models.Professor(**professor.dict())
    db.add(new_professor)
    db.commit()
    db.refresh(new_professor)
    return new_professor

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(id:int, db: Session = Depends(get_db)):
    prof_to_delete = db.query(models.Professor).filter(models.Professor.id == id)
    
    if not prof_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Professor not found")
        
    prof_to_delete.delete(synchronize_session=False)
    db.commit()
    
# @router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ProfessorResponse)
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