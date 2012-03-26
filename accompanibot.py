#!/usr/bin/env python
''' Call this script by passing it the name of a file, each line of which
    is of the format 'wavfilename weight', with weight a real number.
'''

import math
import pprint
import pygame
import random
import sys
import time

TIMESTEP = 0.1
LAMBDA = 2.8

FADE = 5000

def main(fname):
    files_weights = [parseline(li) for li in open(fname, 'r') if parseline(li) is not None]
    normalize_weights(files_weights)
    print 'Using %d audio samples:' % len(files_weights)
    pprint.pprint(files_weights)
    pygame.mixer.init()
    snds = [(pygame.mixer.Sound(fw[0]), fw[1]) for fw in files_weights]
    print 'Using %d channels...' % pygame.mixer.get_num_channels()
    i = 0
    T = 0.0
    while True:
        try:
            #random.choice(snds).play()
            time.sleep(TIMESTEP)
            T += TIMESTEP
            n = pygame.mixer.get_busy()
            if i % 10 == 0:
                print '%d playing (%fs)' % (n, T)
            #prob = 1.0 - poisson_cdf(n)
            prob = 1.0 - logistic(n)
            #print 'n: %f; p: %f; r: %f' % (n, prob, random.random())
            if prob > random.random():
                w_choice(snds).play()
            i += 1
        except KeyboardInterrupt:
            sys.stdout.write("\nFading out...\n")
            sys.stdout.flush()
            pygame.mixer.fadeout(FADE)
            time.sleep(1.0 + (float(FADE) / 1000))
            pygame.mixer.quit()
            sys.exit()

def parseline(line):
    words = line.split()
    if len(words) != 2:
        return None
    return (words[0], float(words[1]))

def normalize_weights(files_weights):
    tot = sum(fw[1] for fw in files_weights)
    for i, (f,w) in enumerate(files_weights):
        files_weights[i] = (f, float(w) / tot)

# from http://snippets.dzone.com/posts/show/732
def w_choice(lst):
    n = random.uniform(0, 1)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item

def logistic(t):
    return 1.0 / (1.0 + math.exp(-LAMBDA * t))

def poisson_cdf(t):
    return 1.0 - math.exp(-LAMBDA * t)

if __name__ == '__main__':
    main(sys.argv[1])
