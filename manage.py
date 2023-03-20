

import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db

from app.database_data.poblate import create_orders
# flake8: noqa
from app.repositories.models import Ingredient, Order, OrderDetail, Size, Beverage, OrderBeverage


manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])


@manager.command('poblate_database')
def poblate_database():
    create_orders()

if __name__ == '__main__':
    manager()
