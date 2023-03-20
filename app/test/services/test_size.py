import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_size_service(create_size):
    # Act
    size = create_size.json

    # Assert
    pytest.assume(create_size.status.startswith('200'))
    pytest.assume(size['_id'])
    pytest.assume(size['name'])
    pytest.assume(size['price'])


def test_update_size_service(client, create_size, size_uri):
    # Arrange
    current_size = create_size.json
    update_data = {**current_size, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    
    # Act
    response = client.put(size_uri, json=update_data)
    
    # Assert
    pytest.assume(response.status.startswith('200'))
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)


def test_get_size_by_id_service(client, create_size, size_uri):
    # Arrange
    current_size = create_size.json
    
    # Act
    response = client.get(f'{size_uri}id/{current_size["_id"]}')
    
    # Assert
    pytest.assume(response.status.startswith('200'))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)


def test_get_sizes_service(client, create_sizes, size_uri):
    # Act
    response = client.get(size_uri)
    
    # Asset
    pytest.assume(response.status.startswith('200'))
    returned_sizes = {size['_id']: size for size in response.json}
    for size in create_sizes:
        pytest.assume(size['_id'] in returned_sizes)
