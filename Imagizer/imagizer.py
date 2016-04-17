import os
import argparse
from threading import Thread
from PIL import Image

# Command build
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="Path to images", default="input/")
parser.add_argument('-d', '--destination', help="Path to rezised images", default="input/smaller/")
parser.add_argument('-ih', '--height', help="Resized image height", default=900)
parser.add_argument('-iw', '--width', help="Resized image width", default=900)
parser.add_argument('-c', '--crop', help="Crop to exact", action="store_true")
parser.add_argument('-v', '--verbose', help="Increase verbosity", action="store_true")
parser.add_argument('-t', '--threads', help="Number of threads", default=4)
args = parser.parse_args()

crop = 0
if args.crop:
    crop = 1

verbose = 0
if args.verbose:
    verbose = 1

filenames = os.listdir(args.input)  # This is the list of files in the input folder


class ImageConverter(Thread):  # ImageConverter shall be subclass of Thread
    def run(self):  # It has run function which is run in a separate thread
        while True:
            try:
                filename = filenames.pop()  # Try to get a filename from the list
            except IndexError:
                break
            if not filename.lower().endswith(".jpg") and not filename.lower().endswith(".png"):
                continue

            if verbose:
                print self.getName(), "is processing", filename

            im = Image.open(os.path.join(args.input, filename))
            width, height = im.size

            if (width > height and not crop) or ((height > width) and crop):
                newWidth = args.width
                newHeight = height * args.width / width
            else:
                newHeight = args.height
                newWidth = width * args.height / height

            resized = im.resize((newWidth, newHeight))
            if crop:
                x0, y0, x1, y1 = resized.getbbox()
                x0 = (x1 - args.width) / 2
                y0 = (y1 - args.height) / 2
                x1 = args.width + x0
                y1 = args.height + y0
                resized = resized.crop((x0, y0, x1, y1))
            resized.save(os.path.join(args.destination, filename))


# Check for destination file. If its not there, create one!
if not os.path.exists(args.destination):
    os.makedirs(args.destination)

# Validate thread count
if args.threads > 16 or args.threads < 0:
    args.threads = 4

# Threads
threads = []
for i in range(0, args.threads):
    threads.append(ImageConverter())
for thread in threads:
    thread.start()  # Start up the threads
for thread in threads:
    thread.join()  # Wait them to finish
