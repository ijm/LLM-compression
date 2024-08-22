import numpy as np
import matplotlib as mpl

from matplotlib.pyplot import subplots
from matplotlib.figure import Figure
from typing import IO

mpl.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": "\n".join([
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         ]),
    'font.size': 9,
    "font.family": "serif",
    })


def stdfig(fig: Figure, file, fmt: str) -> None:
    fig.savefig(file, format=fmt, bbox_inches='tight')


def savefig(fig: Figure, name: str) -> None:
    fig.savefig(name+".pdf", bbox_inches='tight')
    fig.savefig(name+".pgf", bbox_inches='tight')
    fig.savefig(name+".svg", bbox_inches='tight')


# sig:   matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False,
#  sharey=False, squeeze=True, width_ratios=None, height_ratios=None,
#  subplot_kw=None, gridspec_kw=None, **fig_kw)

def fsubplots(*a, **k):
    fig, ax = subplots(*a, **k)
    axl = ax.reshape(-1) if isinstance(ax, np.ndarray) else np.array([ax])

    return fig, axl
