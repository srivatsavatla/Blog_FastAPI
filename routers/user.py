from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
from schemas import User, ShowUser
from models import Users
from hashing import Hash
from typing import List
from sqlalchemy.orm import Session


router=APIRouter()

'''POST methods'''

@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser,
    tags=[
        "users"
    ],  # These tags are sued for seperating the different tags/thigns we are working on.It makes it easier to view it in the UI
)  # Originally if you want to post something then the status code should be 201 not 200 we can change it to 201 using the status from FastAPI to get the correct status.
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = Users(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

'''GET methods'''


@router.get(
    "/user",
    status_code=status.HTTP_200_OK,
    response_model=List[ShowUser],
    tags=["users"],
)
def all_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users


@router.get(
    "/user/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    tags=["users"],
)
def get_user(
    id: int, db: Session = Depends(get_db)
):  # Fast API automatically gives us the response and the db here
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The User with {id} is not present",
        )
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"data":"Thid blog is not present"}
    return user
