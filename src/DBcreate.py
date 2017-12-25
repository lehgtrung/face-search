import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings import DB_NAME, USER, PASSWORD


con = psycopg2.connect(dbname='postgres', user=USER, password=PASSWORD)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute('CREATE DATABASE ' + DB_NAME)
cur.close()
con.close()

con = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD)
cur.execute('CREATE EXTENSION CUBE')
cur.execute('CREATE TABLE TRAIN (id serial, name text, url text, vector cube)')
cur.execute('CREATE TABLE DEV (id serial, name text, url text, vector cube)')
cur.close()
con.close()
