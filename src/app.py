import sys, getopt
from face import *
from face_query import search
from face_detect import generate_faces, detect_face
import os
from db import prepare_db


def main():

    path, img = None, None

    mess = '- To index your images: ' \
              'python app.py -path <path-to-your-images-directory>' \
           '- To search on a certain image: ' \
              'python app.py -image <path-to-your-image>'
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'p:i:h', ['path=', 'image=', 'help'])
    except getopt.GetoptError:
        print mess
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-p', '--path'):
            if os.path.isdir(arg):
                path = arg
            else:
                print 'Path must link to a directory'
                sys.exit(1)

        if opt in ('-i', '--image'):
            if os.path.isfile(arg):
                img = arg
            else:
                print 'Image path must link to a image'
                sys.exit(1)

        if opt in ('-h', '--help'):
            print mess
            sys.exit(2)

    if path:
        print '--SOURCE PATH:' + path

        prepare_db()

        # Create a temporary directory to store cropped face images
        faces_path = '../images/faces'
        generate_faces(path, faces_path)

        # Generate vectors from images and store them in database
        insert_features(faces_path, 'images')

    if img:
        print '--IMAGE PATH:' + img

        # Detect the face from the image
        face_img = detect_face(img)

        # Get the vector from that face
        vector = get_single_predictions(face_img)

        # Show results
        person, time = search(vector)
        print '--PERSON: ' + str(person)
        print '--SEARCH TIME: ' + str(time)


if __name__ == '__main__':
    main()
