from pydantic import BaseModel

"""Has the schema for the request"""


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):  # Used to define the response schema
    title: str
    body: str
    class Config:
        from_attributes = True
    
class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    class Config:
        from_attributes = True