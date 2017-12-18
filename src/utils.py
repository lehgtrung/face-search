import utils


def compute_size(h, w):
    _h, _w = 224 - h, 224 - w
    return _h/2, _w/2


def face_detect(cc, img_path):
    img = utils.imread(img_path)
    gray = utils.cvtColor(img, utils.COLOR_BGR2GRAY)

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


def face_align(face):
    return face


if __name__ == '__main__':
    base_path = '../images/gt_db'

