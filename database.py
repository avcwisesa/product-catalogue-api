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

        user = cls.config['user']
        dbname = cls.config['name']
        host = cls.config['host']
        port = cls.config['port']

        conn_str = f"""
            host={host} port={port} dbname={dbname} user={user}
        """
        return psycopg.connect(conn_str)
