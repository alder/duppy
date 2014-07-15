#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob, sys
from PIL import Image

def image_hash(im):
    image = Image.open(im)
    image = image.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, image.getdata()) / 64.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, image.getdata())),
                  0)

def hamming_distance(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        startpath = sys.argv[1]
    else:
        startpath = ""

    images = glob.glob (startpath+"*.jpg")
    images.extend (glob.glob (startpath+"*.JPG"))
    images.extend (glob.glob (startpath+"*.png"))
    images.extend (glob.glob (startpath+"*.PNG"))
    images.extend (glob.glob (startpath+"*.gif"))
    images.extend (glob.glob (startpath+"*.GIF"))

    count = 1

    print "Start the search for duplicates..."
    print "%d images found in %s" % (len(images), startpath)

    for first_img in images:
        print "[%d of %d] search duplicates for %s:" % (count, len(images), first_img)
        first_hash = image_hash(first_img)
        no_sim = 1
        for i in range (count, len(images)):
            second_img = images[i]
            second_hash = image_hash(second_img)
            dist = hamming_distance(first_hash, second_hash)
            sim = (64 - dist) * 100 / 64
            if sim >= 90:
                print "--- similar image '%s' with hamming distance %d and similarity %d%%" % (second_img, dist, sim)
                no_sim = 0
        if no_sim == 1:
            print "--- no similar images found"
        count += 1
