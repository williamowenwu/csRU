from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from ..storage.database import get_db
from ..domain import validate

router = APIRouter(prefix='/rmp', tags=["Rate My Professor"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_rmp(rmp: validate.ValidateRMP, db: Session = Depends(get_db)):
    return rmp
