import pytest
import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# Create the test database
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Here we create an other dependency for the test database
app.dependency_overrides[get_db] = override_get_db

# Get the FastAPI instance for testing purposes
client = TestClient(app)


def pytest_namespace():
    return {'post_user_r': None}
    return {'post_property_r': None}
    return {'post_property_owner_r': None}


@pytest.fixture
def create_user(autouse=True):
    response = client.get("/users/1")
    if response.status_code == 404:
        pytest.post_user_r = client.post("/users/", json={
            "full_name": "Pierre Dumont",
            "email": "pierre.dumont@gmail.com",
            "age": 45,
            "gender": "M",
            "phone": "0738492567",
            "salary": 2000,
            "job": "waiter"
        })


@pytest.fixture
def create_property(autouse=True):
    response = client.get("/properties/1")
    if response.status_code == 404:
        pytest.post_property_r = client.post("/properties/", json={
            "is_sold": False,
            "is_rented": False,
            "is_available": True,
            "surface": 60,
            "rooms": 2,
            "is_home": False,
            "is_flat": True,
            "age": 20,
            "selling_price": 250000,
            "rental_price": 1500,
            "availability_date": "2020-12-15",
            "adress": "40 boulevard Saint Martin",
            "city": "Paris"
        })


@pytest.fixture
def create_property_owner(autouse=True):
    response = client.get("/properties/1")
    if response.status_code == 404:
        pytest.post_property_owner_r = client.post("/properties/", json={
            "is_sold": False,
            "is_rented": False,
            "is_available": True,
            "surface": 60,
            "rooms": 2,
            "is_home": False,
            "is_flat": True,
            "age": 20,
            "owner_id": 1,
            "selling_price": 250000,
            "rental_price": 1500,
            "availability_date": "2020-12-15",
            "adress": "40 boulevard Saint Martin",
            "city": "Paris"
        })


# ---------------------------------- Unit tests for user operations ----------------------------------


def test_post_valid_user(create_user):
    client.delete("/users/1")
    assert pytest.post_user_r.status_code == 201
    assert pytest.post_user_r.json() == {
        "id": 1,
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@gmail.com",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter",
        'properties': []
    }


def test_post_existing_user(create_user):
    response = client.post("/users/", json={
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@gmail.com",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter"
    })
    client.delete("/users/1")
    assert response.status_code == 400
    assert response.json() == {'detail': 'User already registered'}


def test_get_existing_user(create_user):
    response = client.get("/users/1")
    client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@gmail.com",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter",
        'properties': []
    }


def test_get_unknown_user():
    response = client.get("/users/2")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_put_existing_user(create_user):
    response = client.put("/users/1", json={
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@hotmail.fr",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter"
    })
    client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@hotmail.fr",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter",
        'properties': []
    }


def test_put_unkown_user():
    response = client.put("/users/1", json={
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@hotmail.fr",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter"
    })
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_existing_user(create_user):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "full_name": "Pierre Dumont",
        "email": "pierre.dumont@gmail.com",
        "age": 45,
        "gender": "M",
        "phone": "0738492567",
        "salary": 2000,
        "job": "waiter",
        'properties': []
    }


def test_delete_unknown_user():
    response = client.delete("/users/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


# ---------------------------------- Unit tests for property operations ----------------------------------

def test_post_valid_property(create_property):
    client.delete("/properties/1")
    assert pytest.post_property_r.status_code == 201
    assert pytest.post_property_r.json() == {
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 20,
        "selling_price": 250000,
        "sale_date": None,
        "rental_price": 1500,
        "rental_start_date": None,
        "availability_date": "2020-12-15",
        "owner_id": None,
        "id": 1,
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    }


def test_post_existing_property(create_property):
    response = client.post("/properties/", json={
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 3,
        "is_home": False,
        "is_flat": True,
        "age": 20,
        "selling_price": 250000,
        "rental_price": 1500,
        "availability_date": "2020-12-15",
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    })
    client.delete("/properties/1")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Property already registered'}


def test_post_property_unknown_owner(create_property_owner):
    client.delete("/properties/1")
    assert pytest.post_property_owner_r.status_code == 404
    assert pytest.post_property_owner_r.json(
    ) == {'detail': "The owner id doesn't match any user"}


def test_get_existing_property(create_property):
    response = client.get("/properties/1")
    client.delete("/properties/1")
    assert response.status_code == 200
    assert response.json() == {
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 20,
        "selling_price": 250000,
        "sale_date": None,
        "rental_price": 1500,
        "rental_start_date": None,
        "availability_date": "2020-12-15",
        "owner_id": None,
        "id": 1,
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    }


def test_get_unknown_property():
    response = client.get("/properties/2")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Property not found'}


def test_get_properties_existing_user(create_user, create_property_owner):
    response = client.get("/users/1/properties/")
    client.delete("/users/1")
    client.delete("/properties/1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "is_sold": False,
            "is_rented": False,
            "is_available": True,
            "surface": 60.0,
            "rooms": 2,
            "is_home": False,
            "is_flat": True,
            "age": 20,
            "selling_price": 250000,
            "sale_date": None,
            "rental_price": 1500,
            "rental_start_date": None,
            "availability_date": "2020-12-15",
            "owner_id": 1,
            "id": 1,
            "adress": "40 boulevard Saint Martin",
            "city": "Paris"
        }
    ]


def test_get_properties_unknown_user(create_property_owner):
    response = client.get("/users/1/properties/")
    client.delete("/properties/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_put_existing_property(create_property):
    response = client.put("/properties/1", json={
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 22,
        "selling_price": 250000,
        "rental_price": 1500,
        "availability_date": "2020-12-15"
    })
    client.delete("/properties/1")
    assert response.status_code == 200
    assert response.json() == {
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60.0,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 22,
        "selling_price": 250000,
        "sale_date": None,
        "rental_price": 1500,
        "rental_start_date": None,
        "availability_date": "2020-12-15",
        "owner_id": None,
        "id": 1,
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    }


def test_put_unknown_property():
    response = client.put("/properties/1", json={
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 22,
        "selling_price": 250000,
        "rental_price": 1500,
        "availability_date": "2020-12-15",
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    })
    client.delete("/properties/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Property not found'}


def test_put_property_unknown_owner(create_property):
    response = client.put("/properties/1", json={
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 20,
        "selling_price": 250000,
        "rental_price": 1500,
        "availability_date": "2020-12-15",
        "owner_id": 1
    })
    client.delete("/properties/1")
    assert response.status_code == 404
    assert response.json() == {'detail': "The owner id doesn't match any user"}


def test_put_existing_property_existing_owner(create_property, create_user):
    response = client.put("/properties/1/1", json={
        "owner_id": "1"
    })
    client.delete("/properties/1")
    client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60.0,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 20,
        "selling_price": 250000,
        "sale_date": None,
        "rental_price": 1500,
        "rental_start_date": None,
        "availability_date": "2020-12-15",
        "owner_id": 1,
        "id": 1,
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    }


def test_put_unknown_property_existing_owner(create_user):
    response = client.put("/properties/1/1", json={
        "owner_id": "1"
    })
    client.delete("/users/1")
    assert response.status_code == 404
    assert response.json() == {'detail': "Property not found"}


def test_put_existing_property_unknown_owner(create_property):
    response = client.put("/properties/1/1", json={
        "owner_id": "1"
    })
    client.delete("/properties/1")
    assert response.status_code == 404
    assert response.json() == {'detail': "The owner id doesn't match any user"}


def test_delete_existing_property(create_property):
    response = client.delete("/properties/1")
    assert response.status_code == 200
    assert response.json() == {
        "is_sold": False,
        "is_rented": False,
        "is_available": True,
        "surface": 60,
        "rooms": 2,
        "is_home": False,
        "is_flat": True,
        "age": 20,
        "selling_price": 250000,
        "sale_date": None,
        "rental_price": 1500,
        "rental_start_date": None,
        "availability_date": "2020-12-15",
        "owner_id": None,
        "id": 1,
        "adress": "40 boulevard Saint Martin",
        "city": "Paris"
    }


def test_delete_unkown_property():
    response = client.delete("/properties/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Property not found'}
