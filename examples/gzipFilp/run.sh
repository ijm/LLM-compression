#!/bin/sh -x

P=python
FILE=AStudyInScarlet

$P flip.py -i ../compressor/$FILE.txt -o $FILE.flipped.txt
gzip -9 -c ../compressor/$FILE.txt > $FILE.txt.gz
gzip -9 -c $FILE.flipped.txt > $FILE.flipped.txt.gz

