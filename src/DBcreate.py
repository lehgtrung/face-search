import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings import DB_NAME, USER, PASSWORD
import logging


def prepare_db():
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
    # cur.execute('CREATE TABLE train (id serial, name text, url text, vector cube);')
    # cur.execute('CREATE TABLE dev (id serial, name text, url text, vector cube);')
    cur.execute('CREATE TABLE images (id serial, name text, url text, vector cube);')
    con.commit()
    cur.close()
    con.close()
