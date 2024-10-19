from pydantic import BaseModel
from typing import List,Optional

"""Has the schema for the request"""


class Blog(BaseModel):
    title: str
    body: str

class BlogBase(Blog):
    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    name: str
    email: str
    blogs : List[BlogBase]=[]
    class Config:
        from_attributes = True

class ShowBlog(BaseModel):  # Used to define the response schema
    title: str
    creator: ShowUser

    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
