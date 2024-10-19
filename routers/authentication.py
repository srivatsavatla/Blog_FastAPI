from fastapi import APIRouter,Depends,HTTPException,status
from schemas import Login
from models import Users
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from token import create_access_token

router=APIRouter(tags=['authentication'])


@router.post('/login')
def login(request: Login,db:Session=Depends(get_db)):
    user = db.query(Users).filter(Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")

    access_token = create_access_token(data={"sub": user.email})
    return user
