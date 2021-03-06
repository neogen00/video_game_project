from flask import Flask
import simplejson as json
from flask import request

import src.models as models
import src.db as db
from settings import DB_USER, DB_NAME, DB_HOST, DB_PASSWORD, DEBUG, TESTING


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DB_USER = DB_USER,
        DB_PASSWORD = DB_PASSWORD,
        DATABASE= DB_NAME,
        DB_HOST = DB_HOST,
        DEBUG = DEBUG,
        TESTING = TESTING
    )

    @app.route('/')
    def root_url():
        return 'Welcome to the mobile gaming api'

    @app.route('/games')
    def games_all():
        conn = db.get_db()
        cursor = conn.cursor()

        games = db.find_all(models.Game, cursor)
        game_dicts = [game.__dict__ for game in games]
        return json.dumps(game_dicts, default = str)

    @app.route('/games/<id>')
    def game(id):
        conn = db.get_db()
        cursor = conn.cursor()
        game = db.find(models.Game, id, cursor)
        return json.dumps(game.__dict__, default = str)

    @app.route('/games/earnings/search')
    def games_search_with_earnings():
        conn = db.get_db()
        cursor = conn.cursor()
        params = dict(request.args)
        earnings = models.Earnings.search(params, cursor)
        earnings_dicts = [earning.to_json(cursor) for earning in earnings]
        return json.dumps(earnings_dicts, default = str)

    @app.route('/games/earnings/RPD')
    def games_with_earnings_RPD():
        conn = db.get_db()
        cursor = conn.cursor()
        games = db.find_all(models.Game, cursor)
        games_dicts = [game.to_json(cursor) for game in games]
        return json.dumps(games_dicts, default = str)

    @app.route('/games/rating/<id>')
    def game_with_earnings_ratings(id):
        conn = db.get_db()
        cursor = conn.cursor()
        ratings = db.find_by_game_id(models.Rating, id, cursor)
        ratings_dict = [rating.to_json(cursor) for rating in ratings]
        return json.dumps(ratings_dict, default = str)

    @app.route('/games/all_data')
    def games_with_earnings_ratings():
        conn = db.get_db()
        cursor = conn.cursor()
        ratings = db.find_all(models.Rating, cursor)
        ratings_dicts = [rating.to_json(cursor) for rating in ratings]
        return json.dumps(ratings_dicts, default = str)

    return app