#!/usr/bin/env python3

import argparse
import logging
import sys
from playlanguage.language.interpreter import interpret

def main(args):
    source_code = args.input.read().strip()

    interpret(source_code)
    print()

def entry():
    levels = {
        "d": logging.DEBUG,
        "i": logging.INFO,
        "w": logging.WARNING,
        "e": logging.ERROR,
        "c": logging.CRITICAL 
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("input",type=argparse.FileType("r"),default=sys.stdin,nargs='?')
    parser.add_argument("-l","--level",type=str.lower,choices=levels.keys(),default='w')
    args = parser.parse_args()
    
    logging.basicConfig(level=levels[args.level])

    try:
        main(args)
    finally:
        args.input.close()


if __name__ == "__main__":
    entry()