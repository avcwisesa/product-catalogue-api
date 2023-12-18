from src.model import Product

def test_product_toJSON_valid():
    product = Product(1, 'SKU', 'title', 'BOOK',
                      'NEW', 10, 1000)

    expected = {
        'id': None,
        'sku': product.sku,
        'title': product.title,
        'category': product.category,
        'kondisi': product.kondisi,
        'qty': product.qty,
        'price': product.price
    }

    assert product.toJSON() == expected
