import psycopg

class Database(object):
    config = None

    @classmethod
    def init_db(cls, config):
        cls.config = config

    @classmethod
    def connection(cls):
        if not cls.config:
            raise Exception("DB config not present")

        user = cls.config['database']['user']
        dbname = cls.config['database']['name']
        host = cls.config['database']['host']
        port = cls.config['database']['port']

        conn_str = f"""
            host={host} port={port} dbname={dbname} user={user}
        """
        return psycopg.connect(conn_str)
