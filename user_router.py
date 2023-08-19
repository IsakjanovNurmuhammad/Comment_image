from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import get_db, SessionLocal
from models import User
from schemas import UserSchema, user_read
from typing import List
router = APIRouter()

@router.get("/all-users", response_model=List[user_read])
async def get_all_Users(db: SessionLocal = Depends(get_db)):
    query = db.query(User).all()
    return query


@router.get("/user/{id}", response_model=user_read)
async def get_User(id:int,
                      db: SessionLocal = Depends(get_db)):
    query = db.query(User).filter(User.id == id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    else:
        return query


@router.post("/new-User", response_model=user_read)
async def add_User(schema: UserSchema,
                   db: SessionLocal = Depends(get_db)):
    query = db.query(User).filter(User.name == schema.name).first()
    if query is not None:
        raise HTTPException(status_code=404, detail="User already exist")
    model = User()
    model.name = schema.name
    model.password = schema.password
    model.email = schema.email

    db.add(model)
    db.commit()
    return model

@router.put("/edit-User", response_model=user_read)
async def edit_User(id:int,
                    schema: UserSchema,
                    db: SessionLocal = Depends(get_db),):

    model = db.query(User).filter(User.id == id).first()

    if model is None:
        raise HTTPException(status_code=404, detail="User not Found")
    else:
        model_ = User()
        model_.id = id
        model_.name = schema.name
        model_.password = schema.password
        model_.email = schema.email

        db.add(model)
        db.commit()

        return model_
@router.delete("/User/{id}")
async def del_User(id: int,
                      db: SessionLocal = Depends(get_db)):
    comment = db.query(User).filter(User.id == id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(comment)
    db.commit()
    return "Successfully deleted"
