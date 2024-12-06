from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_sandwich = models.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price
    )
    try:
        db.add(new_sandwich)
        db.commit()
        db.refresh(new_sandwich)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_sandwich


def read_all(db: Session):
    try:
        return db.query(models.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id: int):
    try:
        sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == item_id).first()
        if not sandwich:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return sandwich


def update(db: Session, item_id: int, request):
    try:
        sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == item_id)
        if not sandwich.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")
        update_data = request.dict(exclude_unset=True)
        sandwich.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return sandwich.first()


def delete(db: Session, item_id: int):
    try:
        sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == item_id)
        if not sandwich.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")
        sandwich.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return "Sandwich deleted successfully"
