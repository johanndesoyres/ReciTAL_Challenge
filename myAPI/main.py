from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI instance
app = FastAPI(title="Property management API",
              description="This is a small API to control properties and their owners in a real estate park.")


# Create a dependency with yield, the dependency will allow the creation of only one session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------- User operations --------------------------------------------


# Path operation to create a user, the operation take in input a UserCreate schema
# and return a User schema. We use the db dependecy to have a single session per request,
# open before the request and close when it's finished.
@app.post("/users/",
          response_model=schemas.User,
          status_code=status.HTTP_201_CREATED,
          response_description="The created user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create an user with all the information:

    - **full_name**: name and firstname, UNIQUE and REQUIRED
    - **age**: between 18 and 120
    - **gender**: male or female
    - **phone**: phone number, UNIQUE
    - **job**: current profession
    - **email**: mail adress, UNIQUE and REQUIRED
    - **salary**: monthly salary in euros
    """
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/",
         response_model=List[schemas.User],
         status_code=status.HTTP_200_OK,
         response_description="All users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users.
    """
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}",
         response_model=schemas.User,
         status_code=status.HTTP_200_OK,
         response_description="Selected user")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user with the user id.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@app.put("/users/{user_id}",
         response_model=schemas.User,
         status_code=status.HTTP_200_OK,
         response_description="Updated user")
def change_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update user data with the following fields:

    - **full_name**: name and firstname, UNIQUE and REQUIRED
    - **age**: between 18 and 120
    - **gender**: male or female
    - **phone**: phone number, UNIQUE
    - **job**: current profession
    - **email**: mail adress, UNIQUE and REQUIRED
    - **salary**: monthly salary in euros
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user = crud.update_user(db=db, user=user, user_id=user_id)
    return db_user


@app.delete("/users/{user_id}",
            response_model=schemas.User,
            status_code=status.HTTP_200_OK,
            response_description="Deleted user")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user with the user id.
    """
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


# -------------------------------------------- Property operations --------------------------------------------


@app.post("/properties/",
          response_model=schemas.Property,
          status_code=status.HTTP_201_CREATED,
          response_description="Created property")
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    """
    Create a property with all the information:

    - **adress**: home adress, REQUIRED
    - **city**: city, REQUIRED
    - **is_sold**: boolean, can't be true if "is_rented" is true
    - **is_rented**: boolean, can't be true if "is_sold" is true
    - **is_available**: boolean, can't be true if "is_rented" and "is_sold" are true
    - **surface**: numeric value, must be greater than 0
    - **rooms**: number of rooms, must be greater than 0
    - **is_home**: boolean, can't be equal to "is_flat"
    - **is_flat**: boolean, can't be equal to "is_home"
    - **age**: age of the house, must be greater than 0
    - **selling_price**: selling price, must be greater than 0
    - **sale_date**: datetime
    - **rental_price**: rental price, must be greater than 0
    - **rental_start_date**: datetime
    - **availability_date**: datetime
    - **owner_id** : user id, this id must match one in the user table
    """
    db_property = crud.get_property_by_city_and_adress(
        db=db, city=property.city, adress=property.adress)
    if db_property:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Property already registered")
    if property.owner_id is not None:
        db_user = crud.get_user(db=db, user_id=property.owner_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The owner id doesn't match any user")
    return crud.create_property(db=db, property=property)


# This endpoint is just here for testing purposes, so it will be not displayed in Swagger UI.
@app.get("/properties/{property_id}",
         response_model=schemas.Property,
         status_code=status.HTTP_200_OK,
         response_description="Selected property",
         include_in_schema=False)
def read_property(property_id: int, db: Session = Depends(get_db)):
    """
    Get a property with the property id.
    """
    db_property = crud.get_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return db_property


@app.get("/users/{user_id}/properties/",
         response_model=List[schemas.Property],
         status_code=status.HTTP_200_OK,
         response_description="Selected property")
def read_properties_from_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a property with the property id.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_properties = crud.get_properties_by_owner(db=db, owner_id=user_id)
    return db_properties


@app.put("/properties/{property_id}",
         response_model=schemas.Property,
         status_code=status.HTTP_200_OK,
         response_description="Updated property")
def change_property(property_id: int, property: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    """
    Update property data with the following fields:

    - **adress**: home adress, REQUIRED
    - **city**: city, REQUIRED
    - **is_sold**: boolean, can't be true if "is_rented" is true
    - **is_rented**: boolean, can't be true if "is_sold" is true
    - **is_available**: boolean, can't be true if "is_rented" and "is_sold" are true
    - **surface**: numeric value, must be greater than 0
    - **rooms**: number of rooms, must be greater than 0
    - **is_home**: boolean, can't be equal to "is_flat"
    - **is_flat**: boolean, can't be equal to "is_home"
    - **age**: age of the house, must be greater than 0
    - **selling_price**: selling price, must be greater than 0
    - **sale_date**: datetime
    - **rental_price**: rental price, must be greater than 0
    - **rental_start_date**: datetime
    - **availability_date**: datetime
    - **owner_id** : user id, this id must match one in the user table
    """
    db_property = crud.get_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    if property.owner_id is not None:
        db_user = crud.get_user(db=db, user_id=property.owner_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The owner id doesn't match any user")
    db_property = crud.update_property(
        db=db, property=property, property_id=property_id)
    return db_property


@app.put("/properties/{property_id}/{owner_id}",
         response_model=schemas.Property,
         status_code=status.HTTP_200_OK,
         response_description="Updated property")
def change_property_owner(property_id: int, owner_id: int, db: Session = Depends(get_db)):
    """
    Update a property owner with the property id and the new owner id.
    """
    db_property = crud.get_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Property not found")
    db_user = crud.get_user(db=db, user_id=owner_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The owner id doesn't match any user")
    return crud.update_property_owner(
        db=db, property_id=property_id, owner_id=owner_id)


@app.delete("/properties/{property_id}",
            response_model=schemas.Property,
            status_code=status.HTTP_200_OK,
            response_description="Deleted property")
def remove_property(property_id: int, db: Session = Depends(get_db)):
    """
    Delete a property with the property id.
    """
    db_property = crud.delete_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return db_property
