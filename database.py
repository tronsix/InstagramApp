from psycopg2 import pool

class db: 
    __connection_pool = None

    @classmethod 
    def init(cls, **kwargs):
        cls.connection_pool = pool.SimpleConnectionPool(
            1, 10, **kwargs)
    
    @classmethod
    def get_conn(cls):
        return cls.connection_pool.getconn()

    @classmethod
    def return_conn(cls, connection):
        cls.connection_pool.putconn(connection)

    @classmethod
    def close_conns(cls):
        cls.connection_pool.closeall()

class ConnectionFromPool:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = db.get_conn()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        db.return_conn(self.connection)