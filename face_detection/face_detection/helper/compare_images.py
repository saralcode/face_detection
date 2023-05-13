import face_recognition as fr
import os



def compare_face(file, url):
    # first =  os.path.join(os.getcwd(), file)

    first = os.getcwd() + url
    second = os.getcwd()+file
    # second =   pathlib.Path.joinpath(os.getcwd(), url)

    target_image = fr.load_image_file(file=first)
    target_encoding = fr.face_encodings(target_image)
    known_image = fr.load_image_file(file=second)
    known_encoding = fr.face_encodings(known_image)
    if(known_encoding):
        known_encoding=known_encoding[0]
    is_target_face = fr.compare_faces(
        known_encoding, target_encoding, tolerance=0.4)
    if(is_target_face):
        return is_target_face[0]
    return False

