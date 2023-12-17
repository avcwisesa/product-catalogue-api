from flask import Blueprint
from flask import Flask

import handler
import logging
import tomllib
from argparse import ArgumentParser

if __name__ == "__main__":
    app = Flask(__name__)
    blueprint = Blueprint('blueprint', __name__)

    parser = ArgumentParser()
    parser.add_argument('--env')
    args = parser.parse_args()

    env = args.env
    app.config.update(ENV=env)

    app.config.from_file(f"{env}.toml", load=tomllib.load, text=False)
    app_config = app.config.get_namespace('APP_')

    app.logger.setLevel(logging.INFO)

    app.logger.info(f"Starting {app_config['title']} - {env}")

    blueprint.route('/', methods=['GET'])(handler.index)

    app.register_blueprint(blueprint)
    app.run(debug=True, port=app_config['port'])
