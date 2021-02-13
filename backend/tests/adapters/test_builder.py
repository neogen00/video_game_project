import datetime
from decimal import *
import psycopg2
import pytest

import src.db.db as db
import src.models as models
import src.adapters as adapters
from settings import (DBTEST_USER, DBTEST_NAME, DBTEST_PASSWORD)
from tests.data.builder_data import (TS_details, search_date, rank_type)


@pytest.fixture()
def test_conn():
    test_conn = psycopg2.connect(dbname = DBTEST_NAME, 
            user = DBTEST_USER, password = DBTEST_PASSWORD)
    cursor = test_conn.cursor()
    db.drop_all_tables(test_conn, cursor)
    db.reset_all_primarykey(test_conn, cursor)
    yield test_conn
    db.drop_all_tables(test_conn, cursor)
    db.reset_all_primarykey(test_conn, cursor)


def test_with_non_existing_game(test_conn):
    test_cursor = test_conn.cursor()
    builder = adapters.Builder()
    game_objs = builder.run(TS_details, search_date, rank_type, test_conn, test_cursor)
    game = game_objs['game']
    earnings = game_objs['earnings']
    rating = game_objs['rating']

    assert game.name == 'Among Us'
    assert game.platform == 'android'
    assert game.game_engine == 'Unity'
    assert earnings.revenue == 2000000
    assert earnings.price == 0
    assert rating.TS_rating == Decimal('4.45')
    assert rating.date_created == datetime.date(2020, 12, 28)

def test_with_existing_game(test_conn):
    test_cursor = test_conn.cursor()
    builder = adapters.Builder()
    game_objs = builder.run(TS_details, search_date, rank_type, test_conn, test_cursor)
    game_objs = builder.run(TS_details, search_date, rank_type, test_conn, test_cursor)
    game = game_objs['game']

    assert game.name == 'Among Us'
    assert game.exists == True






