from sqlalchemy.orm import Session
from models import Blogs
from database import get_db
from fastapi import Depends,HTTPException,status
from schemas import Blog

def get_all(db: Session):
    blogs = db.query(Blogs).all()
    return blogs

def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = Blogs(title=request.title, body=request.body, user_id=3)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id : int, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the {id} if nto presenr in the databse",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return {f"Deleted {id}"}


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


def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with {id} is not present",
        )
    return blog
