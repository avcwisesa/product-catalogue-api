import psycopg
from psycopg import sql

DBNAME="product_catalogue_test"
USER="avcwisesa"

con = psycopg.connect(user=USER, host='localhost')
con.autocommit = True

cur = con.cursor()

try:
    db_drop_query = f"DROP DATABASE {DBNAME}"
    cur.execute(sql.SQL(db_drop_query))
except psycopg.errors.InvalidCatalogName:
    pass

db_create_query = f"CREATE DATABASE {DBNAME}"
cur.execute(sql.SQL(db_create_query))
