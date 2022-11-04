from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..domain import schemas
from ..storage import models
from ..storage.database import get_db
from ..auth import utils

router = APIRouter(prefix="/users", tags=["Users"])  # the prefix for all endpoints


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # duplicate = db.query(models.User).filter(models.User.email == user.email).first()

    # if duplicate:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                     detail= "Email Already Exists")
    # hashes the password -> security measure
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with {id} doesn't exist"
        )
    return user
