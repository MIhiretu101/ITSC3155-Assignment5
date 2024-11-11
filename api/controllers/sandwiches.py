from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

def create(db: Session, sandwich):
    # Create a new instance of the Sandwich model with the provided data
    db_sandwich = models.Sandwich(
        name=sandwich.name,
        ingredients=sandwich.ingredients,
        price=sandwich.price
    )
    # Add the new Sandwich object to the database session
    db.add(db_sandwich)

    db.commit()

    db.refresh(db_sandwich)

    return db_sandwich

def read_all(db: Session):
    # Retrieve all sandwiches from the database
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    # Retrieve a specific sandwich by ID
    sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

def update(db: Session, sandwich_id: int, sandwich):
    # Query the database for the specific sandwich to update
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")
    # Extract the update data from the provided 'sandwich' object
    update_data = sandwich.model_dump(exclude_unset=True)
    # Update the database record with the new data
    db_sandwich.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated sandwich record
    return db_sandwich.first()

def delete(db: Session, sandwich_id: int):
    # Query the database for the specific sandwich to delete
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")
    # Delete the database record
    db_sandwich.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)