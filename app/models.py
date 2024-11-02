# app/models.py
from pydantic import BaseModel

class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
