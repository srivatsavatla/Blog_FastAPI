from fastapi import FastAPI
from Blog_FastAPI.schemas import Blog

app = FastAPI()


@app.post("/blog")
def create(request: Blog):
    return {"message": f"Creating a Blog of name {request.title}"}

#ORM(Object relational mapping) means mapping our class/model/object to a table. i.e. 
# we make a class for a table which is reponsible for that table CRUD operations.