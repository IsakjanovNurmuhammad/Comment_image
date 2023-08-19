from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from secrets import token_hex
from db import get_db, SessionLocal
from models import Comment, Comment_image
from typing import List
router = APIRouter()

path = r"C:\Users\Mr_IT\Desktop\Images"

@router.get("/all-images")
async def all_images(db: SessionLocal = Depends(get_db)):
    images = db.query(Comment_image).all()
    return images


@router.get("/get_image")
async def get_image_by_comment_id(comment_id: int,
                                  db: SessionLocal = Depends(get_db)):
    query = db.query(Comment_image).filter(Comment_image.comment_id == comment_id).all()
    if query is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return query


@router.post("/add-image")
async def add_image(comment_id: int,
                    images: List[UploadFile] = File(...),
                    db: SessionLocal = Depends(get_db)):
    query = db.query(Comment).filter(Comment.id == comment_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Image not found.")
    for img in images:
        file_ext = img.filename.split(".").pop()
        file_name = token_hex(10)
        file_path = f"{file_name}.{file_ext}"
        with open(file_path, "wb") as f:
            content = await img.read()
            f.write(content)
        model = Comment_image()
        model.comment_id = comment_id
        model.file_path = file_path
        model.file_name =file_name

        db.add(model)
        db.commit()
        return "Successfully added"


@router.put("/change image")
async def change_img(comment_id: int,
                     images: List[UploadFile] = File(),
                    db: SessionLocal = Depends(get_db)):
    query = db.query(Comment_image).filter(Comment_image.comment_id == comment_id).first()
    if query is None:
        for img in images:
            file_ext = img.filename.split(".").pop()
            file_name = token_hex(10)
            file_path = f"{file_name}.{file_ext}"
            with open(file_path, "wb") as f:
                content = await img.read()
                f.write(content)
            model = Comment_image()
            model.comment_id = comment_id
            model.file_path = file_path
            model.file_name = file_name
            db.add(model)
            db.commit()
            return "Successfully changed"
    db.delete(query)
    for img in images:
        file_ext = img.filename.split(".").pop()
        file_name = token_hex(10)
        file_path = f"{file_name}.{file_ext}"
        with open(file_path, "wb") as f:
            content = await img.read()
            f.write(content)
        model = Comment_image()
        model.comment_id = comment_id
        model.file_path = file_path
        model.file_name = file_name
        db.delete(query)
        db.add(model)
        db.commit()
        return "Successfully changed"


@router.delete("/delete_image")
async def del_image(comment_id: int,
                    db: SessionLocal = Depends(get_db)):
    query = db.query(Comment_image).filter(Comment_image.comment_id == comment_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(query)
    db.commit()
    return "Image successfully deleted."