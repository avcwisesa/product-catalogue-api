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

    def save(self):
        insert_query = f"""
            INSERT INTO product (sku, title, category, kondisi, qty, price)
            VALUES ('{self.sku}', '{self.title}', '{self.category}',
                    '{self.kondisi}', {self.qty}, {self.price})
        """

        with Database.connection() as conn:
            with conn.cursor() as cur:

                cur.execute(sql.SQL(insert_query))

                conn.commit()

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
