from sqlalchemy.orm import Session

from . import models, schemas


# CREATE operation, here we use the Pydantic UserCreate schema for data creation
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    # Add the new SQL alchemy model instance to the database session
    db.add(db_user)
    # commit the changes to the database so they are saved
    db.commit()
    # refresh the instance so it contains generated data by the database like an ID
    db.refresh(db_user)
    return db_user


# READ operation
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_full_name(db: Session, full_name: str):
    return db.query(models.User).filter(models.User.full_name == full_name).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# UPDATE operation, here we use the Pydantic UserUpdate schema for data updating
def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for key, val in user.dict().items():
        setattr(db_user, key, val)
    db.commit()
    return db_user


# DELETE operation
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    else:
        return None


def create_property(db: Session, property: schemas.PropertyCreate):
    db_property = models.Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def get_property(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()


def get_properties_by_owner(db: Session, owner_id: int):
    return db.query(models.Property).filter(models.Property.owner_id == owner_id).all()


def get_property_by_city_and_adress(db: Session, city: str, adress: str):
    return db.query(models.Property).filter(models.Property.city == city).filter(models.Property.adress == adress).first()


def update_property(db: Session, property: schemas.PropertyUpdate, property_id: int):
    db_property = db.query(models.Property).filter(
        models.Property.id == property_id).first()
    for key, val in property.dict().items():
        setattr(db_property, key, val)
    db.commit()
    return db_property


def update_property_owner(db: Session, property_id: int, owner_id: int):
    db_property = db.query(models.Property).filter(
        models.Property.id == property_id).first()
    db_property.owner_id = owner_id
    db.commit()
    return db_property


def delete_property(db: Session, property_id: int):
    db_property = db.query(models.Property).filter(
        models.Property.id == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
        return db_property
    else:
        return None
