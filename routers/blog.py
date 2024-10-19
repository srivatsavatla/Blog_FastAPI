from fastapi import APIRouter, status, Depends, HTTPException
from database import get_db
from schemas import ShowBlog,Blog
from models import Blogs
from typing import List
from sqlalchemy.orm import Session


router=APIRouter()

'''POST methods'''

@router.post(
    "/blog",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowBlog,
    tags=["blogs"],
)  # Originally if you want to post something then the status code should be 201 not 200 we can change it to 201 using the status from FastAPI to get the correct status.
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = Blogs(title=request.title, body=request.body, user_id=3)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


'''GET methods'''


@router.get("/blog", response_model=List[ShowBlog], tags=["blogs"])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(Blogs).all()
    return blogs


@router.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlog,
    tags=["blogs"],
)
def get_blog(
    id: int, db: Session = Depends(get_db)
):  # Fast API automatically gives us the response and the db here
    blog = db.query(Blogs).filter(Blogs.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with {id} is not present",
        )
    return blog


"""DELETE methods"""


@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the {id} if nto presenr in the databse",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return {f"Deleted {id}"}

"""PUT Methods"""

@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the {id} if nto presenr in the databse",
        )
    blog.update(
        request.dict()
    )  # To sue the update function you have to put send it as a dictionary
    db.commit()
    return {"data": "updated title"}
