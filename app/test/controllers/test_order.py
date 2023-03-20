import pytest
from app.controllers import (IngredientController, OrderController,
                             SizeController)
from app.controllers.base import BaseController
from app.test.utils.functions import get_random_choice, shuffle_list


def __order(ingredients: list, size: dict, client_data: dict):
    ingredients = [ingredient.get('_id') for ingredient in ingredients]
    size_id = size.get('_id')
    return {
        **client_data,
        'ingredients': ingredients,
        'size_id': size_id
    }


def __create_items(items: list, controller: BaseController):
    created_items = []
    for ingredient in items:
        created_item, _ = controller.create(ingredient)
        created_items.append(created_item)
    return created_items


def __create_sizes_and_ingredients(ingredients: list, sizes: list):
    created_ingredients = __create_items(ingredients, IngredientController)
    created_sizes = __create_items(sizes, SizeController)
    return created_sizes if len(created_sizes) > 1 else created_sizes.pop(), created_ingredients


def test__create_order__when_functino_get_ingredients_size_and_client_data__should_return_an_order(app, ingredients, size, client_data):
    # Arrange
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    
    # Act
    created_order, error = OrderController.create(order)
    size_id = order.pop('size_id', None)
    ingredient_ids = order.pop('ingredients', [])
    
    # Assert
    pytest.assume(error is None)
    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order['_id'])
        pytest.assume(size_id == created_order['size']['_id'])

        ingredients_in_detail = set(item['ingredient']['_id'] for item in created_order['detail'])
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))


def test__calculate_order_price__when_fucntion_gets_ingredients_size_and_client_data__should_return_the_total_of_all_prices(app, ingredients, size, client_data):
    # Arrange
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    
    # Act
    created_order, _ = OrderController.create(order)
    
    # Assert
    pytest.assume(created_order['total_price'] == round(created_size['price'] + sum(ingredient['price'] for ingredient in created_ingredients), 2))


def test__get_order_by_id__when_function_gets_ingredients_size_and_client_data__should_return_an_order(app, ingredients, size, client_data):
    # Arrange
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    created_order, _ = OrderController.create(order)

    # Act
    order_from_db, error = OrderController.get_by_id(created_order['_id'])
    size_id = order.pop('size_id', None)
    ingredient_ids = order.pop('ingredients', [])
    
    # Assert
    pytest.assume(error is None)
    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order['size']['_id'])

        ingredients_in_detail = set(item['ingredient']['_id'] for item in created_order['detail'])
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))


def test__get_all_orders__when_function_gets_ingredients_sizes_and_client_data__should_return_all_orders(app, ingredients, sizes, client_data):
    # Arrange
    created_sizes, created_ingredients = __create_sizes_and_ingredients(ingredients, sizes)
    created_orders = []
    for _ in range(5):
        order = __order(shuffle_list(created_ingredients)[:3], get_random_choice(created_sizes), client_data)
        created_order, _ = OrderController.create(order)
        created_orders.append(created_order)

    # Act
    orders_from_db, error = OrderController.get_all()
    searchable_orders = {db_order['_id']: db_order for db_order in orders_from_db}
    
    # Assert
    pytest.assume(error is None)
    for created_order in created_orders:
        current_id = created_order['_id']
        assert current_id in searchable_orders
        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)
