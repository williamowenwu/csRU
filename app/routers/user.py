from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils

router = APIRouter(
    prefix="/users", #the prefix for all endpoints
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db:Session = Depends(get_db)):
    duplicate = db.query(models.User).filter(models.User.email == user.email).first()
    
    if duplicate:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail= "Email Already Exists")
    #hashes the password -> security measure
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User with {id} doesn't exist")
    return user