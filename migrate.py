from database import Database
from model import Product

import sys
import tomllib

import jwt
import psycopg
from psycopg import sql

env = sys.argv[1]

with open(f"{env}.toml", "rb") as f:
    config = tomllib.load(f)

    db_config = {
        'name': config['DATABASE_NAME'],
        'user': config['DATABASE_USER'],
        'host': config['DATABASE_HOST'],
        'port': config['DATABASE_PORT']
    }

    Database.init_db(db_config)

    DBNAME = config['DATABASE_NAME']
    USER = config['DATABASE_USER']
    HOST = config['DATABASE_HOST']
    PORT = config['DATABASE_PORT']
    SECRET = config['JWT_SECRET_KEY']

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

conn_str = f"""
    host={HOST} port={PORT} dbname={DBNAME} user={USER}
"""
with psycopg.connect(conn_str) as conn:

    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE tenant (
                id SERIAL NOT NULL PRIMARY KEY,
                name VARCHAR(25) NOT NULL UNIQUE
            );

            CREATE TABLE product (
                id SERIAL NOT NULL PRIMARY KEY,
                tenant SERIAL NOT NULL REFERENCES tenant(id),
                title VARCHAR(30) NOT NULL,
                sku VARCHAR(15) NOT NULL,
                category VARCHAR(15) NOT NULL,
                kondisi VARCHAR(15) NOT NULL,
                qty INTEGER NOT NULL,
                price INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE UNIQUE INDEX idx_product_unique_tenant_sku
            ON product (tenant, sku);

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

            INSERT INTO tenant (name)
            VALUES ('Tenant H');

            INSERT INTO tenant (name)
            VALUES ('Xavier School');
        """)

        conn.commit()

users = [
    {'id': 1, 'name': 'Tenant H'},
    {'id': 2, 'name': 'Xavier School'}
]

for user in users:
    token = jwt.encode(user, SECRET, algorithm='HS256')
    print(f"User: {user['name']}\nToken: {token}")

seeds = [
    Product(1, "ABC-123", "Produk 1", "BOOK", "NEW", 103, 2500),
    Product(1, "ABZ-456", "Produk 2", "COMPUTER", "NEW", 104, 5000),
    Product(1, "ABX-543", "Produk 3", "BAG", "PRE-LOVED", 107, 10000),
    Product(1, "ABX-544", "Produk 4", "BAG", "PRE-LOVED", 107, 11000),
    Product(1, "ABX-545", "Produk 5", "BAG", "NEW", 105, 12000),
    Product(2, "APTX-0001", "buk 001", "BOOK", "NEW", 103, 2500),
    Product(2, "APTX-0002", "comp 002", "COMPUTER", "NEW", 104, 5000),
    Product(2, "APTX-0003", "bag 003", "BAG", "PRE-LOVED", 107, 10000),
    Product(2, "APTX-0004", "bag 004", "BAG", "PRE-LOVED", 107, 11000),
    Product(2, "APTX-0005", "bag 005", "BAG", "NEW", 105, 12000),
    Product(1, "COMPX321", "comp X1", "COMPUTER", "NEW", 100, 100000),
    Product(1, "COMPX322", "comp X2", "COMPUTER", "NEW", 100, 100000),
    Product(1, "COMPX323", "comp X3", "COMPUTER", "NEW", 100, 100000)
]

for seed in seeds:
    seed.save(seed.tenant)
