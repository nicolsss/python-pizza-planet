from app.test.utils.functions import (get_random_sequence, get_random_string, get_random_price, shuffle_list)
import random
import time

def customer_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


def item_data_mock() -> dict():
    return {
        'name': get_random_string(),
        'price': get_random_price(10, 20)
    }


def order_mock(ingredients: list, beverages: list, sizes: list) -> dict():
    size = shuffle_list(sizes)[0]
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence(),
        'ingredients': shuffle_list(ingredients)[:5],
        'beverages': shuffle_list(beverages)[:5],
        'size_id': size['_id']
    }


def crate_date(start_date, end_date, time_format, seed):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + seed * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, seed):
    return crate_date(start, end,"%m/%d/%Y %I:%M %p", random.random())