#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Author       : shiv
Email        : shiv.dutt@tassat.com
Version      : 0.1

Created      : 2021-02-19 14:31
Last Modified: 2021-02-20 20:01:36 EST

Host Machine : chef

Description  :
"""

from __future__ import print_function
from PIL import Image, ImageChops, ImageEnhance
import sys
import os
import argparse
import json
import base64

parser = argparse.ArgumentParser(description="""
Performs Error Level Analysis over a directory of images
""")
parser.add_argument('--dir', dest='directory', required=True,
                    help='path to the directory containing the images')
parser.add_argument('--quality', dest='quality',
                    help='quality used by the jpeg crompression alg.',
                    default=90)
parser.add_argument('--fname', dest='fname', required=True,
                    help='filename in the dir to be tested')

TMP_EXT = ".tmp_ela.jpg"
ELA_EXT = ".ela.png"
SAVE_REL_DIR = "generated"
threads = []
quality = 90


def error_level_analysis(fname, orig_dir, save_dir):
    """
    Generates an ELA image on save_dir.
    Params:
        fname:      filename w/out path
        orig_dir:   origin path
        save_dir:   save path
    """

    print("")
    print("In the ELA function")
    basename, ext = os.path.splitext(fname)

    org_fname = os.path.join(orig_dir, fname)
    print("org_fname is: " + str(org_fname))
    tmp_fname = os.path.join(save_dir, basename + TMP_EXT)
    print("tmp_fname is: " + str(tmp_fname))
    ela_fname = os.path.join(save_dir, basename + ELA_EXT)
    print("ela_fname is: " + str(ela_fname))

    print("")
    print("Opening the image")
    im = Image.open(org_fname)
    im.save(tmp_fname, 'JPEG', quality=quality)

    print("Opening the tmp image")
    tmp_fname_im = Image.open(tmp_fname)
    ela_im = ImageChops.difference(im, tmp_fname_im)
    print("ela_im is: " + str(ela_im))

    extrema = ela_im.getextrema()
    print("extrema is: " + str(extrema))
    max_diff = max([ex[1] for ex in extrema])
    print("max_diff is: " + str(max_diff))
    scale = 255.0/max_diff
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)

    ela_im.save(ela_fname)
    os.remove(tmp_fname)

    return(max_diff)


def main():
    print("In the main function")
    print("Parsing the arguments")
    args = parser.parse_args()
    dirc = args.directory
    fname = args.fname

    ela_dirc = os.path.join(dirc, SAVE_REL_DIR)

    print("Performing ELA on image " + dirc + "/" + fname)

    max_diff = error_level_analysis(fname, dirc, ela_dirc)
    print("")
    print("The max_diff is: " + str(max_diff))
    if(max_diff < 10):
        print("The image is almost certainly not photoshopped (95%  confidence)")
    elif(max_diff >= 10 and max_diff < 15):
        print("The image is more likely not photoshopped")
    elif(max_diff >= 15 and max_diff <= 20):
        print("The image is more likely photoshopped")
    elif(max_diff > 20):
        print("The image is almost certainly photoshopped (95% confidence)")

    print("Check the ELA image at: %s/%s" % (dirc, SAVE_REL_DIR))

    print("")
    print("Writing the JSON payload of the original image to file jayson_payload.txt")
    data = {}
    with open(dirc + "/" + fname, mode='rb') as file:
        img = file.read()
    data['img'] = base64.b64encode(img)
    f = open("json_payload.txt", "a")
    f.write(json.dumps(data))
    f.close()


if __name__ == '__main__':
    main()
else:
    print("This should'nt be imported.", file=sys.stderr)
    sys.exit(1)
