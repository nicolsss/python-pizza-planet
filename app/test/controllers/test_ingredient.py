import pytest
from app.controllers import IngredientController


def test__create_ingredient__when_function_gets_an_ingredient_dict__should_return_a_new_ingredient(app, ingredient: dict):
    # Act
    created_ingredient, error = IngredientController.create(ingredient)
    
    # Assert
    pytest.assume(error is None)
    for param, value in ingredient.items():
        pytest.assume(param in created_ingredient)
        pytest.assume(value == created_ingredient[param])
        pytest.assume(created_ingredient['_id'])


def test__update_ingredient__when_function_gets_an_ingredient__should_return_an_updated_ingredient(app, ingredient: dict):
    # Arrange
    created_ingredient, _ = IngredientController.create(ingredient)
    updated_fields = {
        'name': 'updated',
        'price': 10
    }

    # Act
    updated_ingredient, error = IngredientController.update({
        '_id': created_ingredient['_id'],
        **updated_fields
    })

    # Assert
    pytest.assume(error is None)
    ingredient_from_database, error = IngredientController.get_by_id(created_ingredient['_id'])
    pytest.assume(error is None)
    for param, value in updated_fields.items():
        pytest.assume(updated_ingredient[param] == value)
        pytest.assume(ingredient_from_database[param] == value)


def test__get_ingredient_by_id__when_function_gets_and_ingredient_dict__should_return__an_ingredient(app, ingredient: dict):
    # Arrange
    created_ingredient, _ = IngredientController.create(ingredient)
    
    # Act
    ingredient_from_db, error = IngredientController.get_by_id(created_ingredient['_id'])
    
    # Assert
    pytest.assume(error is None)
    for param, value in created_ingredient.items():
        pytest.assume(ingredient_from_db[param] == value)


def test__get_all_ingredients__when_function_gets_a_ingredient_list__should_return_all_ingredients(app, ingredients: list):
    # Arrange
    created_ingredients = []
    for ingredient in ingredients:
        created_ingredient, _ = IngredientController.create(ingredient)
        created_ingredients.append(created_ingredient)

    # Act
    ingredients_from_db, error = IngredientController.get_all()
    searchable_ingredients = {db_ingredient['_id']: db_ingredient for db_ingredient in ingredients_from_db}
    
    # Assert
    pytest.assume(error is None)
    for created_ingredient in created_ingredients:
        current_id = created_ingredient['_id']
        assert current_id in searchable_ingredients
        for param, value in created_ingredient.items():
            pytest.assume(searchable_ingredients[current_id][param] == value)
