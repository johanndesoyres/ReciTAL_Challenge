from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Numeric, Boolean, Date, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from .database import Base


# SQL Alchemmy model for the user database table
class User(Base):
    __tablename__ = "users"  # Name of the table in the real database

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    full_name = Column(String(50), unique=True, index=True, nullable=False)
    age = Column(Integer)
    gender = Column(Enum('M', 'F', name='gender_types'))
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(50), unique=True)
    salary = Column(Integer)
    job = Column(String(50))

    properties = relationship("Property", back_populates="owner")


# SQL Alchemmy model for the property database table
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    adress = Column(String(50), index=True, nullable=False)
    city = Column(String(50), index=True, nullable=False)
    surface = Column(Numeric)
    rooms = Column(Integer)
    is_home = Column(Boolean, nullable=False, default=True)
    is_flat = Column(Boolean, nullable=False, default=False)
    age = Column(Integer)
    selling_price = Column(Integer)
    sale_date = Column(Date)
    is_sold = Column(Boolean, nullable=False, default=False)
    rental_price = Column(Integer)
    rental_start_date = Column(Date)
    is_rented = Column(Boolean, nullable=False, default=False)
    availability_date = Column(Date)
    is_available = Column(Boolean, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)

    # Two properties can't be located at the same place
    __table_args__ = (UniqueConstraint(
        'adress', 'city', name='_adress_city_uc'),)
    # A property can't be a house and a flat at the same time
    __table_args__ = (CheckConstraint(
        'is_home != is_flat', name='_is_home_is_flat_cc'),)
    # A property can't be sold and rented at the same time
    __table_args__ = (CheckConstraint(
        'is_sold + is_rented <= 1', name='_is_sold_is_rented_cc'),)

    owner = relationship("User", back_populates="properties")
