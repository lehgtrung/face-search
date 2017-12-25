from DBconnect import *
from utils import *
import time


def search(vector, k=10):
    db = DBObject(db=DB_NAME, user=USER, password=PASSWORD)
    q = 'SELECT name from train order by %s <-> vector asc limit %s'
    _vector = AsIs('cube(ARRAY[' + str(vector).strip('[|]') + '])')
    start = time.time()
    results = db.make_query(q, (_vector, str(k)),q_type='query')
    total = time.time() - start
    # return [' '.join(result[0].split('_')[:-1]) for result in results]
    return ' '.join(results[0][0].split('_')[:-1]), total


def accuracy(k=10):
    db = DBObject(db=DB_NAME, user=USER, password=PASSWORD)
    q = 'SELECT name, vector from dev'

    start = time.time()
    dev_images = db.make_query(q, q_type='query')
    total = time.time() - start

    q = 'SELECT name from train order by %s <-> vector asc limit %s'

    count = 0
    for image in dev_images:
        name, vector = image
        _name = '_'.join(name.split('_')[:-1])

        vector = [float(elem) for elem in list(vector.strip('(|)').split(', '))]
        _vector = AsIs('cube(ARRAY[' + str(vector).strip('[|]') + '])')

        candidates = db.make_query(q, (_vector, str(k)), q_type='query')

        most_likely_name = most_common_or_first([candidate[0] for candidate in candidates])

        if most_likely_name.startswith(_name):
            count += 1

    return 1.0*count/len(dev_images), total
