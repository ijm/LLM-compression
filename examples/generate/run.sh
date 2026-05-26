S=../../scripts
P=python3.9

. ../model.sh

export PYTHONPATH=./$S\:$PYTHONPATH

echo -n '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0' | \
  $P -m tokensOfData -n "$MODEL" -c 'Complete a long poem about green trees.' | \
  $P -m modelOfInx -n "$MODEL" -w 128 -cd 0.5 | \
  $P -m tokensToStr -n "$MODEL"
