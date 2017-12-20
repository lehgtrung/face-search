import os
from random import shuffle
from shutil import copyfile


def split_data(src_path, dst_path, ratio=.7):
    train_path = os.path.join(dst_path, 'train/')
    dev_path = os.path.join(dst_path, 'dev/')
    for root, dirs, files in os.walk(src_path):
        for name in dirs:
            dirname = os.path.join(root, name)
            ori_img_names = os.listdir(dirname)

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
                copyfile(os.path.join(dirname, img_name), os.path.join(_train_path, name + '_' + img_name))

            for img_name in dev_images:
                copyfile(os.path.join(dirname, img_name), os.path.join(_dev_path, name + '_' + img_name))


if __name__ == '__main__':
    src_path = '/home/luxeuto/workspace/facesearch/images/slfw_funneled'
    dst_path = '/home/luxeuto/workspace/facesearch/images/data/slfw_funneled'

    split_data(src_path, dst_path)