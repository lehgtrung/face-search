from utils import *
import logging
import cv2


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
