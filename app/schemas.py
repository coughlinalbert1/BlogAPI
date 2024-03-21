from pydantic import BaseModel
from typing import List

# Article object that is inside UserDisplay (what we display to the user)
class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        from_attributes = True 

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []

    class Config():
        from_attributes = True # return database data into our pydantic UserDisplay model

class ArticleBase(BaseModel):
    '''
        Since we defined our relationship with the user.id on the article side, we need it here
        but we will call it creator_id. This is what we recieve from the user when creating an article.
    '''
    title: str
    content: str
    published: bool
    creator_id: int

# User inside article display (what we display to the user)
class User(BaseModel):
    id: int
    username: str

    class Config():
        from_attributes = True # return database data into our pydantic User model

# What we display to the user
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config():
        from_attributes = True # return database data into our pydantic ArticleDisplay model