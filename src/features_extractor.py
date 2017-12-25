from keras_vggface.vggface import VGGFace
from keras.preprocessing import image
from DBconnect import *
from utils import *
from local_binary_patterns import LocalBinaryPatterns


def get_deep_predictions(path, batch_size=1):
    """
    :param path: path to directory containing sub directories of images
    :param model: deep feature extractor model
    :param batch_size: default batch size is 1 due to computer's limitation
    :return: batches and vector representation of each images
    """
    model = VGGFace(include_top=False, input_shape=(3, 224, 224), pooling='max')
    gen = image.ImageDataGenerator(rescale=1./255)

    _batches = gen.flow_from_directory(path, target_size=(224, 224), batch_size=batch_size, shuffle=False)
    _predictions = model.predict_generator(_batches, val_samples=_batches.n)
    return _batches, _predictions


def get_lbp_predictions(path, desc):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(gray)
    return hist


def save_to_db(table, mapper, db):
    """
    :param table: table name
    :param mapper: dictionary mapping from person name to vector representation
    :param db: db object
    :return: None
    """
    for i, key in enumerate(mapper.keys()):
        _name = key
        _url = 'gt_db/' + _name
        _vector = AsIs('cube(ARRAY[' + str(mapper[key].tolist()).strip('[|]') + '])')
        db.make_query("INSERT INTO %s (name, url, vector) VALUES (%s, %s, %s)",
                    (AsIs(table), _name, _url, _vector))

        print str(i) + ' records inserted!'


def insert_deep_features(path, table):
    batches, predictions = get_deep_predictions(path)

    name2vector = {}
    for i, prediction in enumerate(predictions):
        name2vector[batches.filenames[i].split('/')[-1]] = prediction

    db = DBObject(db=DB_NAME, user=USER, password=PASSWORD)
    save_to_db(table, name2vector, db)


def insert_lbp_features(path, table):
    name2vector = {}
    img_paths = load_images(path)
    print len(img_paths)
    desc = LocalBinaryPatterns(510, 8)

    for img_path in img_paths:
        hist = get_lbp_predictions(img_path, desc)
        name2vector[img_path.split('/')[-1]] = hist

    db = DBObject(db=DB_NAME, user=USER, password=PASSWORD)
    save_to_db(table, name2vector, db)

