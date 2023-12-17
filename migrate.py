import psycopg
import sys
import tomllib

from model import Product

from psycopg import sql

env = sys.argv[1]

with open(f"{env}.toml", "rb") as f:
    config = tomllib.load(f)

    DBNAME = config['DATABASE_NAME']
    USER = config['DATABASE_USER']
    HOST = config['DATABASE_HOST']

con = psycopg.connect(user=USER, host=HOST)
con.autocommit = True

cur = con.cursor()

try:
    db_drop_query = f"DROP DATABASE {DBNAME}"
    cur.execute(sql.SQL(db_drop_query))
except psycopg.errors.InvalidCatalogName:
    pass

db_create_query = f"CREATE DATABASE {DBNAME}"
cur.execute(sql.SQL(db_create_query))

with psycopg.connect(f"dbname={DBNAME} user={USER}") as conn:

    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE product (
                id INTEGER NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
                title VARCHAR(30) NOT NULL,
                sku VARCHAR(15) NOT NULL UNIQUE,
                category VARCHAR(15) NOT NULL,
                kondisi VARCHAR(15) NOT NULL,
                qty INTEGER NOT NULL,
                price INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE FUNCTION trigger_set_timestamp()
            RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at=now();
                    RETURN NEW;
                END;
            $$
            LANGUAGE plpgsql;

            CREATE TRIGGER set_timestamp
            BEFORE UPDATE ON product
            FOR EACH ROW
                EXECUTE PROCEDURE trigger_set_timestamp();
        """)

        conn.commit()

seeds = [
    Product("ABC-123", "Produk 1", "cat 1", "kond 1", 3, 2500),
    Product("ABZ-456", "Produk 2", "cat 2", "kond 1", 4, 5000),
    Product("ABX-543", "Produk 3", "cat 3", "kond 2", 7, 10000),
    Product("ABX-544", "Produk 4", "cat 3", "kond 2", 7, 11000),
    Product("ABX-545", "Produk 5", "cat 3", "kond 1", 5, 12000)
]

for seed in seeds:
    seed.save()
