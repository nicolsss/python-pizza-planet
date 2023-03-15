import pytest
from app.controllers import BeverageController


def test_create(app, beverage: dict):
    created_beverage, error = BeverageController.create(beverage)
    pytest.assume(error is None)
    for param, value in beverage.items():
        pytest.assume(param in created_beverage)
        pytest.assume(value == created_beverage[param])
        pytest.assume(created_beverage['_id'])


def test_update(app, beverage: dict):
    return


def test_get_by_id(app, beverage: dict):
    return


def test_get_all(app, beverages: list):
    return
