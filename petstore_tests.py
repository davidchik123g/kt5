import allure
import pytest
from pydantic import BaseModel
import requests


class Pet(BaseModel):
    id: int
    name: str
    status: str


PETSTORE_BASE_URL = "https://petstore.swagger.io/v2"


@pytest.fixture
def generate_pet_data():
    return {"id": 1, "name": "Dog", "status": "available"}


def test_create_pet(generate_pet_data):
    response = requests.post(f"{PETSTORE_BASE_URL}/pet", json=generate_pet_data)
    assert response.status_code == 200

    expected_data = generate_pet_data
    actual_data = response.json()

    with allure.step("Verify the created pet using Pydantic"):
        assert_dict_contains_subset(expected_data, actual_data)


def assert_dict_contains_subset(expected, actual):
    for key, value in expected.items():
        assert key in actual, f"Key '{key}' not found in actual dictionary."
        assert actual[key] == value, f"Value mismatch for key '{key}': expected {value}, got {actual[key]}."


@allure.title("Test Get Pet by ID")
def test_get_pet_by_id():
    pet_id = 1
    response = requests.get(f"{PETSTORE_BASE_URL}/pet/{pet_id}")
    assert response.status_code == 200

    with allure.step(f"Verify the pet with ID {pet_id} using Pydantic"):
        pet = Pet(**response.json())
        assert pet.id == pet_id


@allure.title("Test Delete Pet")
def test_delete_pet():
    pet_id = 1
    response = requests.delete(f"{PETSTORE_BASE_URL}/pet/{pet_id}")
    assert response.status_code == 200

    with allure.step(f"Verify the pet with ID {pet_id} is deleted"):
        response = requests.get(f"{PETSTORE_BASE_URL}/pet/{pet_id}")
        assert response.status_code == 404
