#!/bin/sh -x

S=../../scripts
P=python3.9

export PYTHONPATH=./$S\:$PYTHONPATH

$P -m plotHeatmap -o AStudyInScarlet.html -i ../../examples/compressor/AStudyInScarlet/AStudyInScarlet.ttout.json


