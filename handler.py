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

def update_product(id):
    product = Product.get_by_id(id)

    if product is None:
        return {'error': 'product not found'}, 404

    try:
        product_params = request.get_json()

        if product_params.get('sku') is not None:
            product.sku = product_params.get('sku')

        if product_params.get('title') is not None:
            product.title = product_params.get('title')

        if product_params.get('category') is not None:
            product.category = product_params.get('category')

        if product_params.get('kondisi') is not None:
            product.kondisi = product_params.get('kondisi')

        if product_params.get('price') is not None:
            product.price = product_params.get('price')

        product.update()
    except AttributeError as e:
        return {
            'error': str(e)
        }, 400

    return {'product': product.toJSON()}, 200

def search_product():
    args = request.args
    skus = args.getlist('skus')
    titles = args.getlist('title')
    categories = args.getlist('category')
    conditions = args.getlist('kondisi')

    page_size = int(args.get('page_size'))
    page = int(args.get('page', 1))
    offset = (page - 1) * page_size

    count = Product.get_count(
        skus=skus,
        titles=titles,
        categories=categories,
        conditions=conditions)

    if offset >= count:
        return {'error': 'Page out of range'}, 400

    products = Product.search(
        skus=skus,
        titles=titles,
        categories=categories,
        conditions=conditions,
        limit=page_size,
        offset=offset)

    product_jsons = [product.toJSON() for product in products]

    return {
        'products': product_jsons,
        'page_size': len(product_jsons),
        'page': 1,
        'total': count
    }, 200

def bulk_request():
    bulk_request_params = request.get_json()

    try:
        sku_qty_dict = {
            item['sku']: item['reqQty']
            for item in bulk_request_params['items']
        }

        Product.bulk_qty_update(sku_qty_dict)
    except ValueError as e:
        return {
            'error': str(e)
        }, 400

    return {'status': 'ok'}, 200
