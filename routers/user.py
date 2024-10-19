from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
from schemas import User, ShowUser
from models import Users
from hashing import Hash
from typing import List
from sqlalchemy.orm import Session
from repository import user

router=APIRouter(
    prefix='/user',
    tags=['users']
)

'''POST methods'''

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowUser
    # These tags are sued for seperating the different tags/thigns we are working on.It makes it easier to view it in the UI
)  # Originally if you want to post something then the status code should be 201 not 200 we can change it to 201 using the status from FastAPI to get the correct status.
def create_user(request: User, db: Session = Depends(get_db)):
    return user.create(request,db)

'''GET methods'''


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[ShowUser]
)
def all_users(db: Session = Depends(get_db)):
    return user.get_all(db)

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser
)
def get_user(id: int, db: Session = Depends(get_db)):  # Fast API automatically gives us the response and the db here
    return user.show(id,db)
