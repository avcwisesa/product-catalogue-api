from database import Database

import handler
import logging
import tomllib

from flask import Blueprint
from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(env):
    app = Flask(__name__)
    blueprint = Blueprint('blueprint', __name__)

    app.config.from_file(f"{env}.toml", load=tomllib.load, text=False)
    app_config = app.config.get_namespace('APP_')
    db_config = app.config.get_namespace('DATABASE_')

    Database.init_db(db_config)

    app.logger.setLevel(logging.INFO)
    app.logger.info(f"Starting {app_config['title']} - {env}")

    blueprint.route('/', methods=['GET'])(handler.index)

    blueprint.route("/login", methods=["POST"])(handler.login)

    blueprint.route('/product', methods=['POST'])(handler.create_product)
    blueprint.route('/product', methods=['GET'])(handler.search_product)
    blueprint.route('/product/<int:id>', methods=['GET'])(handler.get_product_by_id)
    blueprint.route('/product/<int:id>', methods=['PATCH'])(handler.update_product)
    blueprint.route('/product/bulk_request', methods=['PATCH'])(handler.bulk_request)

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = app.config['JWT_ACCESS_TOKEN_EXPIRES'] == 'True'

    app.register_blueprint(blueprint)

    JWTManager(app)

    return app
