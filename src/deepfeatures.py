from keras_vggface.vggface import VGGFace
from keras.preprocessing import image
import psycopg2
from psycopg2.extensions import AsIs


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


def get_features(path, dbname, tbname):
    top_model = VGGFace(include_top=False, input_shape=(3, 224, 224), pooling='max')
    batches, predictions = get_predictions(path, top_model)

    name2vector = {}
    for i, prediction in enumerate(predictions):
        name2vector[batches.filenames[i].split('/')[-1]] = prediction

    conn, cur = connect_db(dbname=dbname, user='luxeuto', passwrd='Nuttertools2')
    save_to_db(tbname, name2vector, cur, conn)

    conn.close()


if __name__ == '__main__':
    train_path = '../images/data/mgt_db/train'
    dev_path = '../images/data/mgt_db/dev'
    get_features(train_path, 'facebank2', 'images_train')
    get_features(dev_path, 'facebank2', 'images_dev')
