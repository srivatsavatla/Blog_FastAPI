from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog, ShowBlog, User, ShowUser
from models import Base, Blogs, Users
from database import engine, SessionLocal
from hashing import Hash
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

Base.metadata.create_all(engine)  # Create a table in the database

"""Post methods"""


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


@app.post(
    "/blog",
    status_code=status.HTTP_201_CREATED,
    response_model=ShowBlog,
    tags=["blogs"],
)  # Originally if you want to post something then the status code should be 201 not 200 we can change it to 201 using the status from FastAPI to get the correct status.
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = Blogs(title=request.title, body=request.body,user_id=3)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.post(
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


# ORM(Object relational mapping) means mapping our class/model/object to a table. i.e.
# we make a class for a table which is reponsible for that table CRUD operations.
# db:Session=Depends(get_db) converts the sessionn into  a pydantic thing

"""Get methods"""


@app.get("/")
def index():
    return "Go to the docs page to get more details"


@app.get("/blog", response_model=List[ShowBlog], tags=["blogs"])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(Blogs).all()
    return blogs


@app.get(
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
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"data":"Thid blog is not present"}
    return blog


@app.get(
    "/user",
    status_code=status.HTTP_200_OK,
    response_model=List[ShowUser],
    tags=["users"],
)
def all_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users


@app.get(
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


"""delete methods"""


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
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


"""put methods"""


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
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
