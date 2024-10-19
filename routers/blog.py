from fastapi import APIRouter, status, Depends, HTTPException
from database import get_db
from schemas import ShowBlog,Blog
from models import Blogs
from typing import List
from sqlalchemy.orm import Session
from repository import blog

router=APIRouter(
    prefix='/blog',
    tags=['blogs']
)

'''POST methods'''

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowBlog
)  # Originally if you want to post something then the status code should be 201 not 200 we can change it to 201 using the status from FastAPI to get the correct status.
def create_blog(request: Blog, db: Session = Depends(get_db)):
    return blog.create(request,db)

'''GET methods'''


@router.get("/", response_model=List[ShowBlog])
def get_all_blog(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlog
)
def get_blog(id: int, db: Session = Depends(get_db)):  # Fast API automatically gives us the response and the db here
    return blog.show(id,db)


"""DELETE methods"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return blog.delete(id, db)

"""PUT Methods"""

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)
