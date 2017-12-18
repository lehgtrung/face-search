import psycopg2
from psycopg2.extensions import AsIs
from settings import DBNAME, USER, PASSWORD
from collections import defaultdict

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

    def query(self, query, params=None):
        result = None
        try:
            self._db_cur.execute(query, params)
        except Exception as e:
            print e
        finally:
            return self._db_cur.fetchall()

    def __del__(self):
        self._db_con.close()


def most_common_or_first(names):
    freq = defaultdict(lambda: 0)
    for name in names:
        freq[name] += 1

    most_common = names[0]
    for key in freq.keys():
        if freq[key] > most_common:
            most_common = freq[key]
    return most_common


def search(k=10):
    db = DBObject(db=DBNAME, user=USER, password=PASSWORD)
    q = 'SELECT name, vector from images_dev limit 1000'
    dev_images = db.query(q)

    q = 'SELECT name from images_train order by %s <-> vector asc limit %s'

    count = 0
    for i, image in enumerate(dev_images):
        print i
        name, vector = image
        _name = '_'.join(name.split('_')[:2])

        vector = [float(elem) for elem in list(vector.strip('(|)').split(', '))]
        _vector = AsIs('cube(ARRAY[' + str(vector).strip('[|]') + '])')

        # print 'SELECT name from images_train order by ' + str(_vector) + ' <-> vector asc limit 10'
        candidates = db.query(q, (_vector, str(k)))

        cadi_names = [candidate[0] for candidate in candidates]
        #print cadi_names

        most_likely_name = most_common_or_first([candidate[0] for candidate in candidates])

        if most_likely_name.startswith(_name):
            count += 1
        else:
            print name + '--' + most_likely_name
            print name + '--' + str(cadi_names)

    return count


if __name__ == '__main__':
    print search()


