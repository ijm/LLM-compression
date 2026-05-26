#!/bin/sh -x

S=../../scripts
P=python3.9

. ../../examples/model.sh

F=AStudyInScarlet
export PYTHONPATH=./$S\:$PYTHONPATH

$P -m plotHeatmap -o $F-$TAG.html -i ../../examples/compressor/$F-$TAG/$F.ttout.json
