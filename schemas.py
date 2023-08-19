from pydantic import BaseModel
from fastapi import UploadFile, File

class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class user_read(BaseModel):
    id: int
    name: str
    email: str


class CommentSchema(BaseModel):
    user_id: int
    comment: str


class comment_read(BaseModel):
    id: int
    user_id: int
    comment: str
    image: int
    file_path: str
    file_name: str
