import argparse
import sys


def doArgs(desc: str):
    args = argparse.ArgumentParser(description=desc)

    args.add_argument('-i', '--infile', dest='infile',
                      type=argparse.FileType('rb'), default=sys.stdin.buffer,
                      help='Input file')
    args.add_argument('-o', '--outfile', dest='outfile',
                      type=argparse.FileType('wb'), default=sys.stdout.buffer,
                      help='Output File')

    args.add_argument('-n', '--name', dest='modelname', default=None,
                      help='LLM Model and Tokenizer to use')

    args.add_argument('-w', '--window', dest='contextwindow',
                      default=1020, type=int,
                      help='Max Context window to use')
    args.add_argument('-t', '--topN', dest='topN',
                      default=128, type=int,
                      help='Number of top predicted indexes to keep')

    args.add_argument('-s', '--stopat', dest='count',
                      default=None, type=int,
                      help='maximum number of tokens to process')
    args.add_argument('-c', '--comment', dest='comment', default=None,
                      help='Comment to add to IR file')

    args.add_argument('-p', '--precision', dest='precision',
                      default=32, type=int,
                      help='Size of ints in bits for range and binary encoding'
                      )

    args.add_argument('-f', '--format', dest='format',
                      default="pdf",
                      help='output format for figures')
    args.add_argument('-l', '--limit', dest='numthread',
                      default=None, type=int,
                      help='set number of pytorch threads')
    args.add_argument('-cd', '--cooldown', dest='cooldown',
                      default=0.1, type=float,
                      help='Sleep cooldown at end of intensive steps')

    return args.parse_args()
