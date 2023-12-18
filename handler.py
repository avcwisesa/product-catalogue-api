from model import Product
from model import User

from flask import jsonify
from flask import request
from flask import current_app as app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required

def index():
    app_config = app.config.get_namespace('APP_')
    return {
        'name': app_config['title'],
        'env': app.config['ENV']
    }, 200

def login():
    username = request.json.get("username", None)
    user = User.get_user_by_name(username)
    if not user:
        return jsonify({"msg": "Bad username"}), 401

    additional_claims = {"user_id": user.id}
    access_token = create_access_token(username, additional_claims=additional_claims)
    return jsonify(access_token=access_token)

@jwt_required()
def get_product_by_id(id):
    user_id = get_jwt()['user_id']

    try:
        product = Product.get_by_id(id)

        if user_id != product.tenant:
            return {
                'error': 'Product belongs to other tenant'
            }, 403

        return {
            'product': product.toJSON()
        }, 200
    except:
        return {
            'error': 'Product not found'
        }, 404

@jwt_required()
def create_product():
    user_id = get_jwt()['user_id']

    try:
        product_params = request.get_json()
        new_product = Product.create_from_dict(product_params)
        new_product.tenant = user_id
        product_id = new_product.save()

        new_product.id = product_id
    except AttributeError as e:
        return {
            'error': str(e)
        }, 400

    return {
        'product': new_product.toJSON()
    }, 200

@jwt_required()
def update_product(id):
    user_id = get_jwt()['user_id']
    product = Product.get_by_id(id)

    if user_id != product.tenant:
        return {
            'error': 'Product belongs to other tenant'
        }, 403

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

@jwt_required()
def search_product():
    user_id = get_jwt()['user_id']
    args = request.args
    skus = args.getlist('sku')
    titles = args.getlist('title')
    categories = args.getlist('category')
    conditions = args.getlist('kondisi')

    sort = args.get('sort', 'desc')
    if sort not in ['asc', 'desc']:
        return {
            'error': 'Invalid parameter'
        }, 400
    sort = sort.upper()

    page_size = int(args.get('page_size', 10))
    page = int(args.get('page', 1))
    offset = (page - 1) * page_size

    count = Product.get_count(
        user_id,
        skus=skus,
        titles=titles,
        categories=categories,
        conditions=conditions)

    if offset >= count and page > 1:
        return {'error': 'Page out of range'}, 400

    products = Product.search(
        user_id,
        skus=skus,
        titles=titles,
        categories=categories,
        conditions=conditions,
        limit=page_size,
        offset=offset,
        sort=sort)

    product_jsons = [product.toJSON() for product in products]

    return {
        'products': product_jsons,
        'page_size': len(product_jsons),
        'page': 1,
        'total': count
    }, 200

@jwt_required()
def bulk_request():
    user_id = get_jwt()['user_id']
    bulk_request_params = request.get_json()

    try:
        sku_qty_dict = {
            item['sku']: item['reqQty']
            for item in bulk_request_params['items']
        }

        Product.bulk_qty_update(user_id, sku_qty_dict)
    except ValueError as e:
        return {
            'error': str(e)
        }, 400

    return {'status': 'ok'}, 200
