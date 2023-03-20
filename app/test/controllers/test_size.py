import pytest
from app.controllers import SizeController


def test__create_size__when_function_gets_a_size_dict__should_return_a_new_size(app, size: dict):
    # Act
    created_size, error = SizeController.create(size)
    
    # Assert
    pytest.assume(error is None)
    for param, value in size.items():
        pytest.assume(param in created_size)
        pytest.assume(value == created_size[param])
        pytest.assume(created_size['_id'])


def test__update_size__when_function_gets_a_size_dict__should_return_an_updated_size(app, size: dict):
    # Arrange
    created_size, _ = SizeController.create(size)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }

    # Act
    updated_size, error = SizeController.update({
        '_id': created_size['_id'],
        **updated_fields
    })

    # Assert
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_size[param] == value)


def test__get_by_id_size__when_function_gets_a_size_dict__should_return_a_size(app, size: dict):
    # Arrange
    created_size, _ = SizeController.create(size)
    
    # Act
    size_from_db, error = SizeController.get_by_id(created_size['_id'])
    
    # Assert
    pytest.assume(error is None)
    for param, value in created_size.items():
        pytest.assume(size_from_db[param] == value)


def test__get_all_sizes__when_function_gets_a_list__should_return_all_sizes(app, sizes: list):
    # Arrange
    created_sizes = []
    for size in sizes:
        created_size, _ = SizeController.create(size)
        created_sizes.append(created_size)

    # Act
    sizes_from_db, error = SizeController.get_all()
    searchable_sizes = {db_size['_id']: db_size for db_size in sizes_from_db}
    
    # Assert
    pytest.assume(error is None)
    for created_size in created_sizes:
        current_id = created_size['_id']
        assert current_id in searchable_sizes
        for param, value in created_size.items():
            pytest.assume(searchable_sizes[current_id][param] == value)
