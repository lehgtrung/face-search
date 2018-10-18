import psycopg2
from psycopg2.extensions import AsIs, ISOLATION_LEVEL_AUTOCOMMIT
from settings import DB_NAME, USER, PASSWORD
import logging

class DBObject(object):
    _db_con = None
    _db_cur = None

    def __init__(self, db, user, password):
        try:
            self._db_con = psycopg2.connect(dbname=db, user=user,
                                            password=password)
            self._db_cur = self._db_con.cursor()
        except Exception as e:
            print e

    def make_query(self, query, params=None, q_type='insert'):
        try:
            self._db_cur.execute(query, params)
        except Exception as e:
            print e
        finally:
            if q_type == 'insert':
                self._db_con.commit()
            elif q_type == 'query':
                return self._db_cur.fetchall()

    def __del__(self):
        self._db_con.close()

def prepare_db():
    """
    Create a database with name in .env
    """
    try:
        con = psycopg2.connect(dbname='postgres', user=USER, password=PASSWORD)
    except psycopg2.Error as e:
        raise e
    logging.info('Connected to database postgres')
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute('CREATE DATABASE ' + DB_NAME)
    except psycopg2.Error as e:
        logging.info('DROP OLD DATABASE')
        logging.info('CREATE NEW DATABASE')
        cur.execute('DROP DATABASE ' + DB_NAME)
        cur.execute('CREATE DATABASE ' + DB_NAME)
    cur.close()
    con.close()

    con = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD)
    cur = con.cursor()
    cur.execute('CREATE EXTENSION CUBE')
    cur.execute('CREATE TABLE images (id serial, name text, url text, vector cube);')
    con.commit()
    cur.close()
    con.close()

