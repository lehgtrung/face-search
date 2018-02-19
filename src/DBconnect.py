import psycopg2
from psycopg2.extensions import AsIs


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


