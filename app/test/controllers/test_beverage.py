import pytest
from app.controllers import BeverageController


def test__create_beverage__when_function_have_a_beverage_dict__should_return_a_new_created_service(app, beverage: dict):
    # Act
    created_beverage, error = BeverageController.create(beverage)
    
    # Assert
    pytest.assume(error is None)
    for param, value in beverage.items():
        pytest.assume(param in created_beverage)
        pytest.assume(value == created_beverage[param])
        pytest.assume(created_beverage['_id'])


def test__update_beverage__when_function_have_a_beverage_dict__should_return_a_updated_beverage(app, beverage: dict):
    # Arrage
    created_beverage, _ = BeverageController.create(beverage)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }
    
    # Act
    updated_beverage, error = BeverageController.update({
        '_id': created_beverage['_id'],
        **updated_fields
    })

    # Assert
    pytest.assume(error is None)
    beverage_from_db, error = BeverageController().get_by_id(created_beverage['_id'])
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_beverage[param] == value)
        pytest.assume(beverage_from_db[param] == value)


def test__get_beverage_by_id__when_have_a_beverage_dict__should_return_a_beverage(app, beverage: dict):
    # Arrange
    created_beverage, _ = BeverageController.create(beverage)
    
    # Act
    beverage_from_db, error = BeverageController().get_by_id(created_beverage['_id'])
    
    # Assert
    pytest.assume(error is None)
    for param, value in created_beverage.items():
        pytest.assume(beverage_from_db[param] == value)


def test__get_all_beverages__when_have_a_list_should_return_all_beverages(app, beverages: list):
    # Arrange
    created_beverages = []
    for beverage in beverages:
        created_beverage, _ = BeverageController.create(beverage)
        created_beverages.append(created_beverage)

    # Act
    beverages_from_db, error = BeverageController().get_all()
    searchable_beverages = {db_beverage['_id']: db_beverage for db_beverage in beverages_from_db}
    
    # Assert
    pytest.assume(error is None)
    for created_beverage in created_beverages:
        current_id = created_beverage['_id']
        assert current_id in searchable_beverages
        for param, value in created_beverage.items():
            pytest.assume(searchable_beverages[current_id][param] == value)
