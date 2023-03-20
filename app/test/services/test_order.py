import pytest


def test_create_order_service(create_order):
    # Act
    order = create_order.json
    
    # Assert
    pytest.assume(create_order.status.startswith('200'))
    pytest.assume(order['_id'])
    pytest.assume(order['client_address'])
    pytest.assume(order['client_dni'])
    pytest.assume(order['client_name'])
    pytest.assume(order['client_phone'])
    pytest.assume(order['date'])
    pytest.assume(order['detail'])
    pytest.assume(order['beverages'])
    pytest.assume(order['size'])
    pytest.assume(order['total_price'])


def test_get_order_by_id_service(client, create_order, order_uri):
    # Arrange
    current_order = create_order.json
    
    # Act
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    
    # Assert
    pytest.assume(response.status.startswith("200"))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)


def test_get_orders_service(client, create_orders, order_uri):
    # Act
    response = client.get(order_uri)
    
    # Assert
    pytest.assume(response.status.startswith("200"))
    returned_orders = {order["_id"]: order for order in response.json}
    for order in create_orders:
        pytest.assume(order["_id"] in returned_orders)
