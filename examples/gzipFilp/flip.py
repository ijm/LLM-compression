from argparse import ArgumentParser, FileType
import re
import sys


def doArgs(desc: str):
    args = ArgumentParser(description=desc)

    args.add_argument('-i', '--infile', dest='infile',
                      type=FileType('r'), default=sys.stdin,
                      help='Input file')
    args.add_argument('-o', '--outfile', dest='outfile',
                      type=FileType('w'), default=sys.stdout,
                      help='Output File')

    return args.parse_args()


def main():
    def flip(m):
        return m[1] + m[2].swapcase()

    args = doArgs("Post Dot Case Flip")

    indata = args.infile.read()
    outdata = re.sub(r"(\.\s+)([A-Za-z])", flip, indata)

    args.outfile.write(outdata)


if __name__ == "__main__":
    main()
