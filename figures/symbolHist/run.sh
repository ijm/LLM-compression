#!/bin/sh -x

S=../../scripts
P=python3.9

. ../../examples/model.sh

F=AStudyInScarlet
export PYTHONPATH=./$S\:$PYTHONPATH

$P -m plotTokenHist -o $F-$TAG.hist.svg -f 'svg' -i ../../examples/compressor/$F-$TAG/$F.ttout.json
