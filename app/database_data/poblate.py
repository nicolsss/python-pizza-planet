from ..database_data import constants
from app.controllers import IngredientController,  BeverageController, SizeController, OrderController
from ..database_data.utils import ( item_data_mock, random_date, order_mock)


import json

def create_ingredients(total_ingredients=constants.TOTAL_INGREDIENTS):
    for _ in range(total_ingredients):
        IngredientController.create(item_data_mock())


def create_beverages(total_beverages=constants.TOTAL_BEVERAGES):
    for _ in range(total_beverages):
        BeverageController.create(item_data_mock())


def create_sizes(total_sizes=constants.TOTAL_SIZES):
    for _ in range(total_sizes):
        SizeController.create(item_data_mock())


def create_orders(total_orders=constants.TOTAL_ORDERS):
    create_beverages()
    create_ingredients()
    create_sizes()

    ingredients, _ = IngredientController().get_all()
    ingredients = [ingredient.get('_id') for ingredient in ingredients]
    
    beverages, _ = IngredientController().get_all()
    beverages = [beverage.get('_id') for beverage in beverages]

    sizes, _ =   SizeController.get_all()
    
    for _ in range(total_orders):
       order = order_mock(ingredients, beverages, sizes)
       OrderController().create(order)
