from utils import *
import sys, getopt
from utils import *
from features_extractor import *
from face_query import accuracy, search
from face_detect import generate_faces


def main():
    path = None
    input_img = None
    dump_file = None
    method = 'deep'
    work_path = '../images/data/final'
    temp_path = '../images/data/temp'
    try:
        opts,_ = getopt.getopt(sys.argv[1:], 'p:i:d:m', ['path=',
                                                         'input=', 'dumpfile=', 'method='])
    except getopt.GetoptError:
        print 'USAGE: python app.py -p <imagespath> -i <inputimage> -d <dumpfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-p', '--path'):
            path = arg
        if opt in ('-i', '--input'):
            input_img = arg
        if opt in ('-d', '--dumpfile'):
            dump_file = arg if arg else '../file/dumpfile.psql'
        if opt in ('-m', '--method'):
            method = arg

    if path: print '--SOURCE PATH:' + path
    if input_img: print '--INPUT IMAGE:' + input_img
    if dump_file: print '--DUMP FILE:' + dump_file
    if method: print '--METHOD:' + method

    if not input_img:
        if path:
            split_data(path, temp_path)
            generate_faces(temp_path + '/train', work_path + '/train')
            generate_faces(temp_path + '/dev', work_path + '/dev')
            if method == 'deep':
                print '--USING DEEP FEATURES EXTRACTOR'
                insert_deep_features(work_path + '/train', 'train')
                insert_deep_features(work_path + '/dev', 'dev')
            if method == 'lbp':
                print '--USING LOCAL BINARY PATTERNS FEATURES EXTRACTOR'
                insert_lbp_features(work_path + '/train', 'train')
                insert_lbp_features(work_path + '/dev', 'dev')
            print '--SEARCH ACCURACY: ' + str(accuracy()[0]*100) + '%'
            print '--SEARCH TIME: ' + str(accuracy()[1]) + '(ms)'
        elif dump_file:
            print '--SEARCH ACCURACY: ' + str(accuracy()[0] * 100) + '%'
            print '--SEARCH TIME: ' + str(accuracy()[1]) + '(ms)'
    else:
        if path:
            generate_faces(path, work_path + '/general')
            vector = None
            if method == 'deep':
                print '--USING DEEP FEATURES EXTRACTOR'
                insert_deep_features(work_path + '/general', 'gen')
                input_dir = '/'.join(input_img.split('/')[:-2])
                vector = get_deep_predictions(input_dir)[1][0].tolist()
            if method == 'lbp':
                print '--USING LOCAL BINARY PATTERNS FEATURES EXTRACTOR'
                insert_lbp_features(work_path + '/general', 'gen')
                vector = get_lbp_predictions(input_img, LocalBinaryPatterns(510, 8))
            print '--SEARCH RESULT: ' + search(vector)[0]
            print '--SEARCH TIME: ' + search(vector)[1] + '(ms)'
        elif dump_file:
            vector = None
            if method == 'deep':
                print '--USING DEEP FEATURES EXTRACTOR'
                input_dir = '/'.join(input_img.split('/')[:-2])
                vector = get_deep_predictions(input_dir)[1][0].tolist()
            if method == 'lbp':
                print '--USING LOCAL BINARY PATTERNS FEATURES EXTRACTOR'
                insert_lbp_features(work_path + '/general', 'gen')
                vector = get_lbp_predictions(input_img, LocalBinaryPatterns(510, 8))
            print '--SEARCH RESULT: ' + search(vector)[0]
            print '--SEARCH TIME: ' + search(vector)[1] + '(ms)'


if __name__ == '__main__':
    main()
