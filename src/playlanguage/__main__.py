import argparse
import sys
import interpreter.tokens as tokens

def main(args):
    stack = []
    operations = []
    builder = tokens.TokenBuilder(stack)
    operations.append(builder.build_push(70))
    operations.append(builder.build_push(1))
    operations.append(builder.build_subtract())
    operations.append(builder.build_pop())
    for token in operations:
        print(token())

def entry():
    parser = argparse.ArgumentParser()
    parser.add_argument("input",type=argparse.FileType("r"),default=sys.stdin,nargs='?')
    args = parser.parse_args()
    
    try:
        main(args)
    finally:
        args.input.close()


if __name__ == "__main__":
    entry()