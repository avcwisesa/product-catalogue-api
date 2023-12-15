import psycopg
import sys
import tomllib

from psycopg import sql

env = sys.argv[1]

with open(f"{env}.toml", "rb") as f:
    config = tomllib.load(f)

    DBNAME = config['database']['name']
    USER = config['database']['user']

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
