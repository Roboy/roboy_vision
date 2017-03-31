# Downloads and extracts all necessary models
# TF Checkpoint for facenet trained on MS-Celeb 1M
# MTCNN for face detection and alignment model
# Pre-calculated embeddings on LFW using facenet with dlib face recognizer and alignment
#
# Currently hosted on dropbox of schoenertf@gmail.com
#


import zipfile
import io
from urllib.request import urlopen
url = urlopen("https://www.dropbox.com/s/p9bm5wf1s0r0vmo/models.zip?dl=1")
zipfile = zipfile.ZipFile(io.BytesIO(url.read()))
zipfile.extractall('./')
zipfile.close()