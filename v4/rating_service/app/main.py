from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .db import get_db
from pydantic import BaseModel
from .auth import get_current_user

class RatingUpdate(BaseModel):
    stars: int

app = FastAPI(title="Rating Service")

@app.get("/manage/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/rating", response_model=schemas.UserRatingResponse)
def get_rating(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    username = user["sub"]
    rating = (
        db.query(models.Rating)
        .filter(models.Rating.username == username)
        .first()
    )

    if rating is None:
        raise HTTPException(
            status_code=404,
            detail="Rating not found",
        )

    return rating

@app.patch("/api/v1/rating")
def update_rating(body: RatingUpdate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    username = user["sub"]
    rating = (
        db.query(models.Rating)
        .filter(models.Rating.username == username)
        .first()
    )

    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    rating.stars = max(1, min(100, body.stars))

    db.commit()
    db.refresh(rating)

    return {
        "stars": rating.stars
    }