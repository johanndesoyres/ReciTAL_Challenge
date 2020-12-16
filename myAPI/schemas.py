from datetime import date
from enum import Enum

from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator


# Enum class for the gender field
class GenderEnum(str, Enum):
    male = 'M'
    female = 'F'


class PropertyBase(BaseModel):
    """
    Basic Pydantic schema for the property.
    """
    is_sold: bool = False
    is_rented: bool = False
    is_available: bool = True
    surface: Optional[float] = Field(gt=0)
    rooms: Optional[int] = Field(gt=0)
    is_home: bool = True
    is_flat: bool = False
    age: Optional[int] = Field(ge=0)
    selling_price: Optional[int] = Field(gt=0)
    sale_date: Optional[date] = None
    rental_price: Optional[int] = Field(gt=0)
    rental_start_date: Optional[date] = None
    availability_date: Optional[date] = None
    owner_id: Optional[int] = Field(gt=0)

    @validator('is_flat')
    def check_is_home_is_flat_integrity(cls, is_flat: bool, values: Dict[str, Optional[str]]):
        is_home = values.get('is_home')
        if is_home == is_flat:
            raise ValueError(
                'The property need to be a home or a flat, please set up correctly these fields')
        return is_flat

    @validator('is_rented')
    def check_is_sold_is_rented_integrity(cls, is_rented: bool, values: Dict[str, Optional[str]]):
        is_sold = values.get('is_sold')
        if is_sold is True and is_rented is True:
            raise ValueError(
                "The property can't be sold or rented at the same time, please set up correctly these fields")
        return is_rented


class PropertyCreate(PropertyBase):
    """
    Pydantic schema to create a property.
    """
    adress: str = Field(max_length=50)
    city: str = Field(max_length=50)


class PropertyUpdate(PropertyBase):
    """
    Pydantic schema to update a property.
    """
    pass


class Property(PropertyBase):
    """
    Pydantic schema to read a property.
    """
    id: int
    adress: str = Field(max_length=50)
    city: str = Field(max_length=50)

    # Required to validate from ORMs
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """
    Basic Pydantic schema for the user.
    """
    full_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    age: Optional[int] = Field(None, ge=18, le=120)
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = Field(None, max_length=50)
    salary: Optional[int] = Field(None, gt=0)
    job: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """
    Pydantic schema to create a user.
    """
    pass


class UserUpdate(UserBase):
    """
    Pydantic schema to update a user.
    """
    pass


class User(UserBase):
    """
    Pydantic schema to read a user.
    """
    id: int
    properties: List[Property] = []

    class Config:
        orm_mode = True
