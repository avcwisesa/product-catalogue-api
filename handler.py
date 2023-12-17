from model import Product

from flask import request
from flask import current_app as app

def index():
    app_config = app.config.get_namespace('APP_')
    return {
        'name': app_config['title'],
        'env': app.config['ENV']
    }, 200

def get_product_by_id(id):
    try:
        product = Product.get_by_id(id)
        return {
            'product': product.toJSON()
        }, 200
    except:
        return {}, 404

def create_product():
    try:
        product_params = request.get_json()
        new_product = Product.create_from_dict(product_params)
        product_id = new_product.save()

        new_product.id = product_id
    except AttributeError as e:
        return {
            'error': str(e)
        }, 400

    return {
        'product': new_product.toJSON()
    }, 200
