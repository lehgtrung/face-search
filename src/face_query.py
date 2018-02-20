from DBconnect import *
from utils import *
import time
from settings import DB_NAME, USER, PASSWORD


def search(vector, k=10):
    """
        vector: numpy array vector

        Return: predicted name of the face and search time
    """
    db = DBObject(db=DB_NAME, user=USER, password=PASSWORD)
    q = 'SELECT name from images order by vector <-> %s asc limit %s'
    _vector = AsIs('cube(ARRAY[' + ','.join(str(vector).strip('[|]').split()) + '])')
    start = time.time()
    try:
        results = db.make_query(q, (_vector, str(k)),q_type='query')
    except Exception as e:
        raise e
    total = time.time() - start
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
