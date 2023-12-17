from database import Database

from psycopg import sql
from psycopg import errors

config = {
    "database": {
        "user": "avcwisesa",
        "name": "product_catalogue_test",
        "port": 5432,
        "host": "localhost"
    }
}
Database.init_db(config)

class Product():
    CATEGORIES = ['BOOK', 'COMPUTER', 'BAG']
    CONDITIONS = ['NEW', 'PRE-LOVED']

    def __init__(self, sku, title, category, kondisi, qty, price, id=None):
        self.id = id
        self.sku = sku
        self.title = title
        self.category = category
        self.kondisi = kondisi
        self.qty = qty
        self.price = price

    @classmethod
    def get_by_id(cls, id):
        get_query = f"""
            SELECT sku, title, category, kondisi, qty, price, id
            FROM product WHERE id = {id}
        """

        with Database.connection() as conn:

            with conn.cursor() as cur:

                cur.execute(sql.SQL(get_query))
                result = cur.fetchone()

                if result is None:
                    return None
                else:
                    return Product(*result)

    @classmethod
    def search(cls, skus=None, titles=None, categories=None, conditions=None,
               limit=10, offset=0):
        products = []

        select_columns = "sku, title, category, kondisi, qty, price, id"
        search_query = cls._search_query(select_columns, skus, titles, categories, conditions)
        search_query += " ORDER BY created_at DESC"
        if limit != -1:
            search_query += f" LIMIT {limit} OFFSET {offset}"

        with Database.connection() as conn:

            with conn.cursor() as cur:

                cur.execute(sql.SQL(search_query))
                results = cur.fetchall()

                products = [Product(*result) for result in results]

        return products

    @classmethod
    def get_count(cls, skus=None, titles=None, categories=None, conditions=None):
        select_columns = "count(1)"
        search_query = cls._search_query(select_columns, skus, titles, categories, conditions)

        count = 0
        with Database.connection() as conn:

            with conn.cursor() as cur:

                cur.execute(sql.SQL(search_query))
                count = cur.fetchone()[0]

        return count

    @classmethod
    def bulk_qty_update(cls, sku_qty_dict):
        req_skus = list(sku_qty_dict.keys())
        products = cls.search(skus=req_skus, limit=-1)
        available_sku_qty_dict = {
            product.sku: product.qty for product in products
        }
        available_skus = set(list(available_sku_qty_dict.keys()))

        unavailable_skus = set(req_skus) - available_skus
        if len(unavailable_skus) > 0:
            raise ValueError(f"SKU(s) not found: {unavailable_skus}")

        insufficient_qty_skus = []
        for req_sku, req_qty in sku_qty_dict.items():
            if req_qty > available_sku_qty_dict[req_sku]:
                insufficient_qty_skus.append(req_sku)

        if insufficient_qty_skus:
            raise ValueError(f"Insufficient qty for SKU(s): {insufficient_qty_skus}")

        available_sku_id_dict = {
            product.sku: product.id for product in products
        }
        update_requests = [
            (available_sku_qty_dict[req_sku] - req_qty, available_sku_id_dict[req_sku]) 
            for req_sku, req_qty in sku_qty_dict.items()]

        query = """
            UPDATE product SET qty = %s WHERE id = %s;
        """

        with Database.connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, update_requests)
                conn.commit()

    @classmethod
    def create_from_dict(self, param_dict):
        new_product = Product(
            param_dict.get('sku', None),
            param_dict.get('title', None),
            param_dict.get('category', None),
            param_dict.get('kondisi', None),
            param_dict.get('qty', None),
            param_dict.get('price', None)
        )

        return new_product

    @classmethod
    def _search_query(cls, columns="*", skus=None, titles=None, categories=None, conditions=None):
        search_query = f"""
            SELECT {columns}
            FROM product
        """

        search_parameters = []

        if skus:
            search_parameters.append(f"""sku IN (\'{ "','".join(skus) }\')
                                     """)

        if titles:
            search_parameters.append(f"""title IN (\'{ "','".join(titles) }\')
                                     """)

        if categories:
            search_parameters.append(f"""category IN (\'{ "','".join(categories) }\')
                                     """)

        if conditions:
            search_parameters.append(f"""kondisi IN (\'{ "','".join(conditions) }\')
                                     """)

        if search_parameters:
            search_query += f" WHERE { ' AND '.join(search_parameters) }"

        return search_query

    def save(self):
        insert_query = f"""
            INSERT INTO product (sku, title, category, kondisi, qty, price)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        self._validate()

        product_id = None
        with Database.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(insert_query, self._get_insert_args())
                    product_id = cur.fetchone()[0]
                    conn.commit()
                except errors.UniqueViolation:
                    raise AttributeError(f"Duplicated SKU: {self.sku}")

        return product_id

    def update(self):
        update_query = """
            UPDATE product
            SET sku = %s,
                title = %s,
                category = %s,
                kondisi = %s,
                price = %s
            WHERE id = %s;
        """

        self._validate()

        with Database.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(update_query, self._get_update_args())
                conn.commit()

    def toJSON(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'title': self.title,
            'category': self.category,
            'kondisi': self.kondisi,
            'qty': self.qty,
            'price': self.price
        }

    def _validate(self):
        if (self.sku is None or self.title is None or self.category is None or
            self.kondisi is None or self.qty is None or self.price is None):
            raise AttributeError("Missing product parameter")

        if self.kondisi not in Product.CONDITIONS:
            raise AttributeError(f"Invalid kondisi: {self.kondisi}")

        if self.category not in Product.CATEGORIES:
            raise AttributeError(f"Invalid category: {self.category}")

    def _get_insert_args(self):
        return (self.sku, self.title, self.category,
                self.kondisi, self.qty, self.price)

    def _get_update_args(self):
        return (self.sku, self.title, self.category,
                self.kondisi, self.price, self.id)
