from flask import Blueprint
from flask import Flask

app = Flask(__name__)

def index():
    return "<p>Product Catalogue API</p>"

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)

app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
