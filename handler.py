from model import Product

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
