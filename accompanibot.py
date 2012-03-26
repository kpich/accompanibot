#!/usr/bin/env python
''' Call this script by passing it some number of directories containing
    wav files. It will (nonrecursively) find all *.wav files in those
    directories.
'''

import itertools
import math
import os
import pprint
import pygame
import random
import sys
import time

MIN_SIMULTANEOUS = 1
MAX_SIMULTANEOUS = 8

TIMESTEP = 0.1
LAMBDA = 2.0

def main(dirs):
    files = [x for x in itertools.chain(*[[os.path.join(d, f) for f in os.listdir(d)]
                                          for d in dirs])]
    files = [x for x in files if x.endswith('.wav')]
    print 'Using %d audio samples:' % len(files)
    pprint.pprint(files)
    pygame.mixer.init()
    snds = [pygame.mixer.Sound(f) for f in files]
    print 'Using %d channels...' % pygame.mixer.get_num_channels()
    stop = False
    while True:
        #random.choice(snds).play()
        time.sleep(TIMESTEP)
        n = pygame.mixer.get_busy()
        print '%d playing' % n
        prob = 1.0 - poisson_cdf(n)
        print 'n: %f; p: %f; r: %f' % (n, prob, random.random())
        if prob > random.random():
            if not stop:
                random.choice(snds).play()
    #pygame.mixer.quit()

def poisson_cdf(t):
    return 1.0 - math.exp(-LAMBDA * t)

if __name__ == '__main__':
    main(sys.argv[1:])
