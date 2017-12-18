import cv2
import os


def compute_size(h, w):
    _h, _w = 224 - h, 224 - w
    return _h/2, _w/2


def face_detect(cc, img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cc.detectMultiScale(gray, 1.3, 5)
    roi_color = None

    if len(faces) == 0:
        print 'No face found'
        return roi_color
    else:
        x,y,w,h = faces[0]
        _h, _w = compute_size(h, w)
        roi_color = img[y - _h:y + h + _h, x - _w:x + w + _w]

    return roi_color


def flow_all(cc, src_path, dst_path):
    for root, dirs, files in os.walk(src_path):
        for name in dirs:
            dirname = os.path.join(root, name)
            images = os.listdir(dirname)
            images = [image for image in images if image.endswith('jpg')]

            _path = os.path.join(dst_path, name)

            if not os.path.exists(_path):
                os.makedirs(_path)

            for image in images:
                print image
                face = face_detect(cc, os.path.join(dirname, image))
                if face is None: continue
                cv2.imwrite(os.path.join(_path, image), face)


if __name__ == '__main__':
    src_path = '/home/luxeuto/workspace/facesearch/images/data/gt_db/'
    dst_path = '/home/luxeuto/workspace/facesearch/images/data/mgt_db/'

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    flow_all(face_cascade, src_path + 'train', dst_path + 'train')
    flow_all(face_cascade, src_path + 'dev', dst_path + 'dev')