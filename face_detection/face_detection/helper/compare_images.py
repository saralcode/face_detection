import face_recognition as fr
import pathlib
import os
from django.core.files.base import ContentFile
import urllib.request as ur


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




# def find_target_face():
#     # face_location = fr.face_locations(target_image)
#     for person in encode_faces('face_recog/faces/'):
#         try:
#             encoded_face = person [0]
#             filename = person [1]
#             is_target_face = fr.compare_faces(encoded_face, target_encoding, tolerance=0.55)
#             print(f"{is_target_face[0]} {filename}")
#         except:
#             print("Error ")
