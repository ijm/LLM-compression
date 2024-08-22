#!/bin/sh -x

S=../../scripts
P=python3.9

export PYTHONPATH=./$S\:$PYTHONPATH

$P -m plotTokenHist -o AStudyInScarlet.hist.svg -f 'svg' -i ../../examples/compressor/AStudyInScarlet/AStudyInScarlet.ttout.json


