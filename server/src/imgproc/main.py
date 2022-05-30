import os
import sys
import argparse
from glob import glob
#from PIL import Image, ImageDraw
from PIL import Image


def run_one(opts, idx, inputFile, outputDir):
    path, fileName = os.path.split(inputFile)
    baseName, _ = os.path.splitext(fileName)
    outName = os.path.join(outputDir, f"{baseName}") + '.jpg'
    factor = 0.1
    with Image.open(inputFile) as im:
        (width, height) = (int(im.width * factor), int(im.height * factor))
        im_resized = im.resize((width, height))
        im_resized.show()
        im_resized.save(outName, format="JPEG", quality=75, progressive=True)



def run(opts, inputDir, outputDir):
    for idx, inputFile in enumerate(glob(inputDir + "/*.jpg")):
        run_one(opts, idx, inputFile, outputDir)


#canvas = Image.new('RGB', (400, 300), 'white')
#img_draw = ImageDraw.Draw(canvas)
#img_draw.rectangle((70, 50, 270, 200), outline='red', fill='blue')
#img_draw.text((70, 250), 'Hello World', fill='green')
#canvas.save('drawn_image.jpg')



def main():
    opts = []
    run(opts, "static/images-big", "static/images")


if __name__ == '__main__':
    main()
