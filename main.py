from fastapi import FastAPI
from models import Base
from database import engine
from routers import blog, user


app = FastAPI()

Base.metadata.create_all(engine)  # Create a table in the database

app.include_router(blog.router)
app.include_router(user.router)
@app.get("/")
def index():
    return "Go to the docs page to get more details"
