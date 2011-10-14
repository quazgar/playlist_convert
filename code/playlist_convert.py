#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Originally meant to convert Amarok playlists."""

# from random import choice
# from string import ascii_lowercase
# import readline
# import re
import sys
import parse_k3b
import parse_amarok

def main():
    inFileName = sys.argv[1]
    # print inFileName
    # inFile = open(inFileName)
    tracks = None
    if inFileName.endswith('.k3b'):
        tracks = parse_k3b.parse(inFileName)
    else:
        tracks = parse_amarok.parse(inFileName)
    return 0

if __name__ == '__main__':
    main()



