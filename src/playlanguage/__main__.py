#!/usr/bin/env python3
'''Handler for command line functionality.'''

import argparse
import logging
from playlanguage.language.interpreter import Interpreter

def main(args: argparse.Namespace):
    '''Main function.
    :param args: Command line arguments.
    :type args: argparse.Namespace'''
    source_code = args.input.read().strip()

    interpreter = Interpreter(source_code)
    interpreter.interpret()
    print()

def entry():
    '''Command line entry point.'''
    levels = {
        "d": logging.DEBUG,
        "i": logging.INFO,
        "w": logging.WARNING,
        "e": logging.ERROR,
        "c": logging.CRITICAL
    }

    parser = argparse.ArgumentParser(prog="playlanguage", \
        description="Interpreter for the Playlanguage.")
    parser.add_argument("input", type=argparse.FileType("r"), \
        help="Input file.")
    parser.add_argument("-l", "--level", type=str.lower, \
        choices=levels.keys(), default='w', help="Logging level.")
    args = parser.parse_args()

    logging.basicConfig(level=levels[args.level])

    try:
        main(args)
    finally:
        args.input.close()


if __name__ == "__main__":
    entry()
