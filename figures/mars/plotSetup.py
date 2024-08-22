import matplotlib as mpl
import argparse

mpl.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": "\n".join([
        r"\usepackage[utf8x]{inputenc}",
        r"\usepackage[T1]{fontenc}",
    ])
}
# r"\usepackage{cmbright}",
mpl.rcParams.update({'font.size': 9, "font.family": "serif", })
mpl.rcParams.update(pgf_with_pdflatex)
import matplotlib.pyplot as plt  # noqa: E402
#  import matplotlib.ticker as ticker  # noqa: E402 ;  for custom ticks
#  from matplotlib import colors  # noqa: E402 ; for custom colourmaps


def doArgsPlaceHolder():
    parser = argparse.ArgumentParser(description="Plot profiles")
    parser.add_argument('-p', '--polys', dest='pname',
                        required=True, help='polynomials file')
    return parser.parse_args()


def mkFig(nrows: int, ncols: int):
    fig, ax = plt.subplots(nrows, ncols)
    return fig, ax

# sig:   matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, width_ratios=None, height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw)


def savefig(fig, name):
    fig.savefig(name + ".pdf", bbox_inches='tight')
    fig.savefig(name + ".pgf", bbox_inches='tight')
    fig.savefig(name + ".svg", bbox_inches='tight')

