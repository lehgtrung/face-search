from keras_vggface.vggface import VGGFace
from keras.preprocessing import image
import psycopg2
from psycopg2.extensions import AsIs
from local_binary_patterns import LocalBinaryPatterns
import os
import cv2, numpy as np


def connect_db(dbname, user, passwrd):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=passwrd)
        cur = conn.cursor()
        return conn, cur
    except:
        print "I am unable to connect to the database"
        return False


def get_predictions(img_dir, model):
    gen = image.ImageDataGenerator(rescale=1./255)

    _batches = gen.flow_from_directory(img_dir, target_size=(224, 224), batch_size=1, shuffle=False)
    _predictions = model.predict_generator(_batches, val_samples=_batches.n)
    return _batches, _predictions


def save_to_db(tbname, mapper, cur, conn):
    for i, key in enumerate(mapper.keys()):
        _name = key
        _url = 'gt_db/' + _name
        _vector = AsIs('cube(ARRAY[' + str(mapper[key].tolist()).strip('[|]') + '])')
        cur.execute("INSERT INTO %s (name, url, vector) VALUES (%s, %s, %s)",
                    (AsIs(tbname), _name, _url, _vector))

        print str(i) + ' records inserted!'
    conn.commit()


def get_deep_features(path, dbname, tbname):
    top_model = VGGFace(include_top=False, input_shape=(3, 224, 224), pooling='max')
    batches, predictions = get_predictions(path, top_model)

    name2vector = {}
    for i, prediction in enumerate(predictions):
        print i
        name2vector[batches.filenames[i].split('/')[-1]] = prediction

    conn, cur = connect_db(dbname=dbname, user='luxeuto', passwrd='Nuttertools2')
    save_to_db(tbname, name2vector, cur, conn)

    conn.close()


def load_images(path):

    img_paths = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            dirname = os.path.join(root, name)
            local_paths = [os.path.join(dirname, image) for image in os.listdir(dirname)]
            img_paths.extend(local_paths)
    return img_paths


def get_lbp_features(path, dbname, tbname):
    name2vector = {}
    img_paths = load_images(path)
    print len(img_paths)
    desc = LocalBinaryPatterns(510, 8)

    for i, img_path in enumerate(img_paths):
        print i
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)

        name2vector[img_path.split('/')[-1]] = hist

    conn, cur = connect_db(dbname=dbname, user='luxeuto', passwrd='Nuttertools2')
    save_to_db(tbname, name2vector, cur, conn)

    conn.close()


if __name__ == '__main__':
    train_path = '/home/luxeuto/workspace/facesearch/images/data/slfw_funneled/train'
    dev_path = '/home/luxeuto/workspace/facesearch/images/data/slfw_funneled/dev'
    #get_deep_features(train_path, 'facebank3', 'images_train')
    #get_deep_features(dev_path, 'facebank3', 'images_dev')

    get_lbp_features(dev_path, 'facecbank_lbp', 'images_dev')
    get_lbp_features(train_path, 'facecbank_lbp', 'images_train')
