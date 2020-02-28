import io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import sys
import glob
import os

image_dir = sys.argv[1]
text_dir = sys.argv[2]

dirlist = []
dirlist = glob.glob(os.path.join(image_dir, '*.jpg'))

for file in dirlist:
    client = vision.ImageAnnotatorClient()
    with io.open(file, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        annotation = response.full_text_annotation

        out = os.path.join(text_dir, os.path.basename(file).rstrip('.jpg')+ '.txt')
        with open(out, 'w') as outfile:
            outfile.write(annotation.text.encode('utf8'))
