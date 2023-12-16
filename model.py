from database import Database

from psycopg import sql

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

        search_query = cls._search_query(skus, titles, categories, conditions)
        search_query += f"ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"

        with Database.connection() as conn:

            with conn.cursor() as cur:

                cur.execute(sql.SQL(search_query))
                results = cur.fetchall()

                products = [Product(*result) for result in results]

        return products

    @classmethod
    def _search_query(cls, skus=None, titles=None, categories=None, conditions=None):
        search_query = f"""
            SELECT sku, title, category, kondisi, qty, price, id
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
        """

        with Database.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(insert_query, self._get_insert_args())
                conn.commit()

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

        with Database.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(update_query, self._get_update_args())
                conn.commit()

    def _get_insert_args(self):
        return (self.sku, self.title, self.category,
                self.kondisi, self.qty, self.price)

    def _get_update_args(self):
        return (self.sku, self.title, self.category,
                self.kondisi, self.price, self.id)
