import io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import sys
import glob
import os

image_dir = sys.argv[1]
annotation_dir = sys.argv[2]

dirlist = []
dirlist = glob.glob(os.path.join(image_dir, '*.jpg'))

for file in dirlist:
    client = vision.ImageAnnotatorClient()
    with io.open(file, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        document = response.full_text_annotation

        out = os.path.join(annotation_dir, os.path.basename(file).rstrip('.jpg')+ '.tsv')
        with open(out, 'w') as outfile:
            outfile.write('\t'.join(['content', 'x', 'y', 'w', 'h', '\n']))
            for page in document.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            for symbol in word.symbols:
                                content = symbol.text.encode('utf8')
                                top_left = symbol.bounding_box.vertices[0]
                                bottom_right = symbol.bounding_box.vertices[2]
                                x = top_left.x
                                y = top_left.y
                                w = abs(bottom_right.x - top_left.x)
                                h = abs(bottom_right.y - top_left.y)
                                outfile.write('\t'.join([content, str(x), str(y), str(w), str(h), '\n']))


'''
bounding_box {
  vertices {
    x: 827 # top left
    y: 186
  }
  vertices {
    x: 906 # top right
    y: 186
  }
  vertices {
    x: 906 # bottom right
    y: 421
  }
  vertices {
    x: 827 # bottom left
    y: 421
  }
}
'''
