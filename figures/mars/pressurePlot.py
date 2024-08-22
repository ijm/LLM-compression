import argparse
import numpy as np
from plotSetup import mkFig, savefig
import math
from scipy.optimize import curve_fit


def doArgs():
    parser = argparse.ArgumentParser(description="Plot")
    parser.add_argument('-i', '--infile', dest='infile',
                        required=True, help='input data file')
    parser.add_argument('-o', '--outfile', dest='outfile',
                        required=True, help='output file basename')
    return parser.parse_args()


def main():
    args = doArgs()

    with open(args.infile) as f:
        data = f.read()

    lines = data.split("\n")
    arr = [x.split() for x in lines]
    data = np.array([(float(x[2]), float(x[4])) for x in arr
                    if len(x) > 2 and x[0] == 'VL1' and float(x[4]) > -9])

    def f(x, a, b, c, d, e):
        ls = x * math.pi / 180.0
        return e + a * np.sin(c + 2.0 * ls) + b * np.sin(d + ls)

    params = curve_fit(f, data[:, 0], data[:, 1])
    (a, b, c, d, e) = params[0]
    print(params)
    xs = np.linspace(0, 360, 60)
    ys = f(xs, a, b, c, d, e)

    fig, ax = mkFig(1, 1)

    ax.scatter(data[:, 0], data[:, 1], s=0.1, c='r')
    ax.plot(xs, ys, c='black')
    ax.set_xlim((0, 360))
    ax.set_ylim((6.5, 9.5))
    ax.set_xlabel("Time of year ($L_s$ angle around orbit)")
    ax.set_ylabel("Pressure (mbar)")
    fig.set_size_inches(6, 2)
    savefig(fig, args.outfile)


if __name__ == "__main__":
    main()
