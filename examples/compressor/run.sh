# This script should build the data directory in its entirety.
# Note modelToInx and modelOfInx take a long time to run.
# Note intemediate directory is made inplace.
#
# This is ment to build the files once for the article. It is not a
# makefile, so it should be easy to modify or cut'n'pase.

S=../../scripts
P=python3.9

# Base name of file to process - should be an arguement
#
F=$(basename "$1" .txt)
export PYTHONPATH=./$S\:$PYTHONPATH

# directory for intemediates is the basename of the file
mkdir -p $F

$P -m tokensOfStr -n gpt2 -i $F.txt -o $F/$F.toksout.json
$P -m modelToInx -w 1023 -cd 0.5 -n gpt2 -i $F/$F.toksout.json -o $F/$F.ttout.json
$P -m rangeEncode -i $F/$F.ttout.json -o $F/$F.rangedout.json
$P -m binOfRange -i $F/$F.rangedout.json -o $F.bin

$P -m binToRange -i $F.bin -o $F/$F.rangedin.json
$P -m rangeDecode -i $F/$F.rangedin.json -o $F/$F.ttin.json
$P -m modelOfInx -w 1023 -cd 0.5 -n gpt2 -i $F/$F.ttin.json -o $F/$F.toksin.json
$P -m tokensToStr -n gpt2 -i $F/$F.toksin.json -o $F.decomp.txt

