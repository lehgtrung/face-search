from keras_vggface.vggface import VGGFace
from keras.preprocessing import image
from db import DBObject
from psycopg2.extensions import AsIs
from settings import DB_NAME, USER, PASSWORD, TABLE
import numpy as np
import logging
import cv2
from utils import *


def detect_face(img_path, cc_path='../files/haarcascade_frontalface_default.xml'):
    """
    Detect the face from the image, return colored face
    """

    cc = cv2.CascadeClassifier(os.path.abspath(cc_path))
    img_path = os.path.abspath(img_path)
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cc.detectMultiScale(gray, 1.3, 5)
    roi_color = None

    if len(faces) == 0:
        logging.exception(img_path + ': No face found')
    else:
        x,y,w,h = faces[0]
        _h, _w = compute_size(h, w)
        roi_color = img[y - _h:y + h + _h, x - _w:x + w + _w]

    return roi_color


def generate_faces(src_path, dst_path):
    """
    Generate faces from source directory and store cropped faces in destination directory
    """
    for root, dirs, files in os.walk(src_path):
        for name in dirs:
            dir_name = os.path.join(root, name)
            images = os.listdir(dir_name)
            images = [image for image in images if image.endswith('jpg')]

            _path = os.path.join(dst_path, name)

            if not os.path.exists(_path):
                os.makedirs(_path)

            for image in images:
                face = detect_face(os.path.join(dir_name, image))
                if face is None: continue
                cv2.imwrite(os.path.join(_path, image), face)

def get_single_predictions(face_img):
    """
        face_img: cropped face image, type: numpy array

        Return: vector representation of the face
    """
    if face_img.shape[2] == 3:
        face_img = face_img.transpose((-1, 0, 1))
    face_img = face_img[np.newaxis, ...]
    model = VGGFace(include_top=False, input_shape=(3, 224, 224), pooling='max')
    prediction = model.predict(face_img)
    return prediction


def get_batch_predictions(path, batch_size=32):
    """
        Path: path to the image directory
        batch_size: default batch size is 32

        Return: batches and vector representation of each images
    """
    model = VGGFace(include_top=False, input_shape=(3, 224, 224), pooling='max')
    gen = image.ImageDataGenerator(rescale=1./255)

    _batches = gen.flow_from_directory(path, target_size=(224, 224), batch_size=batch_size, shuffle=False)
    _predictions = model.predict_generator(_batches, val_samples=_batches.n)
    return _batches, _predictions


def save_to_db(table, mapper, db):
    """
        table: table name
        mapper: dictionary mapping from person name to vector representation
        db: db object
    """
    for i, key in enumerate(mapper.keys()):
        _name = key
        _url = 'gt_db/' + _name
        _vector = AsIs('cube(ARRAY[' + str(mapper[key].tolist()).strip('[|]') + '])')
        db.make_query("INSERT INTO %s (name, url, vector) VALUES (%s, %s, %s)",
                    (AsIs(table), _name, _url, _vector))

        print str(i) + ' records inserted!'


def insert_features(path, table):
    batches, predictions = get_batch_predictions(path)

    name2vector = {}
    for i, prediction in enumerate(predictions):
        name2vector[batches.filenames[i].split('/')[-1]] = prediction

    db = DBObject(db=DB_NAME, user=USER, password=PASSWORD)
    save_to_db(table, name2vector, db)