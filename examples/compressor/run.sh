# This script should build the data directory in its entirety.
# Note modelToInx and modelOfInx take a long time to run.
# Note intemediate directory is made inplace.
#
# This is ment to build the files once for the article. It is not a
# makefile, so it should be easy to modify or cut'n'pase.

S=../../scripts
P=python3.9

. ../model.sh

# Base name of file to process - should be an arguement
#
F=$(basename "$1" .txt)
OUT="${F}-${TAG}"
export PYTHONPATH=./$S\:$PYTHONPATH

# directory for intemediates is the basename of the file
mkdir -p $OUT

$P -m tokensOfStr -n "$MODEL" -i $F.txt -o $OUT/$F.toksout.json
$P -m modelToInx -w 1023 -cd 0.5 -n "$MODEL" -i $OUT/$F.toksout.json -o $OUT/$F.ttout.json
$P -m rangeEncode -i $OUT/$F.ttout.json -o $OUT/$F.rangedout.json
$P -m binOfRange -i $OUT/$F.rangedout.json -o $OUT.bin

$P -m binToRange -i $OUT.bin -o $OUT/$F.rangedin.json
$P -m rangeDecode -i $OUT/$F.rangedin.json -o $OUT/$F.ttin.json
$P -m modelOfInx -w 1023 -cd 0.5 -n "$MODEL" -i $OUT/$F.ttin.json -o $OUT/$F.toksin.json
$P -m tokensToStr -n "$MODEL" -i $OUT/$F.toksin.json -o $OUT.decomp.txt
