import numpy as np

from json import loads

from arguments import doArgs
from figurePlotSetup import stdfig, fsubplots
from utils import buildSymTableRanges


def main():
    args = doArgs("Plot histogram of indexes after modeling")
    topN = args.topN

    json = loads(args.infile.read())

    token_tupples: list[int] = json["tokenList"]

    # Anything that isn't in the topN index positions is a miss so -1
    msg = [-1 if i == -1 or i > topN else i for (t, i, p) in token_tupples]

    inx_to_sym, counts = buildSymTableRanges(msg)

    data = np.array([inx_to_sym, counts], dtype=float)

    data[1, :] *= 100. / np.sum(data[1, :])

    fig, ax = fsubplots(1)
    ax = ax[0]

    ax.bar(data[0, :], data[1, :],
           width=0.5, align='center',
           alpha=0.5, color='black',
           )
    #  ax.set_yscale('log')
    ax.set_xlabel("Index")
    ax.set_ylabel("% of Symbols")
    ax.set_xlim(-2, 40)
    fig.set_size_inches(10, 3)

    stdfig(fig, args.outfile, args.format)


main()
