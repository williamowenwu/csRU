from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from ..schemas import Token
from ..models import User
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(
    tags=['Authentication']
)


# authentication
@router.post('/login', response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    database_user = db.query(User).filter(User.email == user.username).first()

    if not database_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    if not verify(user.password, database_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    access_token = create_access_token(data={"user_id": database_user.id})

    return {"access_token": access_token,
            "token_type": "bearer"
            }
