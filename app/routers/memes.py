from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/memes", response_model=list[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_memes(db, skip=skip, limit=limit)

@router.get("/memes/{meme_id}", response_model=schemas.Meme)
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme

@router.post("/memes", response_model=schemas.Meme)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.create_meme(db, meme=meme)

@router.delete("/memes/{meme_id}", response_model=schemas.Meme)
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.delete_meme(db, meme_id=meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme

@router.put("/memes/{meme_id}", response_model=schemas.Meme)
def update_meme(meme_id: int, meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    db_meme = crud.update_meme(db, meme_id=meme_id, meme=meme)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme
