import os
from collections import defaultdict
from random import shuffle
from shutil import copyfile


def most_common_or_first(objs):
    freq = defaultdict(lambda: 0)
    for obj in objs:
        freq[obj] += 1

    most_common = objs[0]
    for key in freq.keys():
        if freq[key] > most_common:
            most_common = freq[key]
    return most_common


def load_images(path):

    img_paths = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            dir_name = os.path.join(root, name)
            local_paths = [os.path.join(dir_name, image) for image in os.listdir(dir_name)]
            img_paths.extend(local_paths)
    return img_paths


def compute_size(h, w):
    _h, _w = 224 - h, 224 - w
    return _h/2, _w/2


def split_data(src_path, dst_path, ratio=.7):
    train_path = os.path.join(dst_path, 'train/')
    dev_path = os.path.join(dst_path, 'dev/')
    for root, dirs, files in os.walk(src_path):
        for name in dirs:
            dir_name = os.path.join(root, name)
            ori_img_names = os.listdir(dir_name)

            shuffle(ori_img_names)
            offset = int(ratio * len(ori_img_names))

            train_images = ori_img_names[:offset]
            dev_images = ori_img_names[offset:]

            _train_path = os.path.join(train_path, name)
            _dev_path = os.path.join(dev_path, name)

            if not os.path.exists(_train_path):
                os.makedirs(_train_path)

            if not os.path.exists(_dev_path):
                os.makedirs(_dev_path)

            for img_name in train_images:
                copyfile(os.path.join(dir_name, img_name), os.path.join(_train_path, name + '_' + img_name))

            for img_name in dev_images:
                copyfile(os.path.join(dir_name, img_name), os.path.join(_dev_path, name + '_' + img_name))
