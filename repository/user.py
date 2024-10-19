from fastapi import status, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from schemas import User
from models import Users
from hashing import Hash


def create(request: User, db: Session = Depends(get_db)):
    new_user = Users(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users

def show(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The User with {id} is not present",
        )
    return user
