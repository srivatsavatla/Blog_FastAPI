from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog,ShowBlog
from models import Base, Blogs
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()


def get_db():
    """function is used to create a new SQLAlchemy database session for each request."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  # Re-raise the exception so FastAPI can handle it properly
    finally:
        db.close()


Base.metadata.create_all(engine)  # Create a table in the database


@app.post(
    "/blog", status_code=status.HTTP_201_CREATED
)  # Originally if you want to post something then the status code should be 201 not 200 we can change it to 201 using the status from FastAPI to get the correct status.
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = Blogs(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# ORM(Object relational mapping) means mapping our class/model/object to a table. i.e.
# we make a class for a table which is reponsible for that table CRUD operations.
# db:Session=Depends(get_db) converts the sessionn into  a pydantic thing


@app.get("/blog",response_model=List[ShowBlog])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(Blogs).all()
    return blogs


@app.get("/blog/{id}", status_code=200,response_model=ShowBlog)
def get_blog(
    id, db: Session = Depends(get_db)
):  # Fast API automatically gives us the response and the db here
    blog = db.query(Blogs).filter(Blogs.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with {id} is not present",
        )
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"data":"Thid blog is not present"}
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the {id} if nto presenr in the databse",
        )
    blog.update(request)
    db.commit()
    return {"data": "updated title"}
