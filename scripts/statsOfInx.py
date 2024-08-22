import numpy as np

from json import loads

from arguments import doArgs
from utils import buildSymTableRanges


def main():
    args = doArgs("Stats from model output json")
#    modelname = args.modelname or "gpt2"
    topN = args.topN

#      tokenizer = GPT2Tokenizer.from_pretrained(modelname)

    json = loads(args.infile.read())

    token_tupples: list[int] = json["tokenList"]

    msg = [-1 if i == -1 or i > topN else i for (t, i, p) in token_tupples]

    inx_to_sym, counts = buildSymTableRanges(msg)
    data = np.array([inx_to_sym, counts], dtype=float)

    total = np.sum(data[1, :])
    mdata = np.array(msg)

    misses = mdata[mdata < 0].shape[0]
    hits = mdata[mdata >= 0].shape[0]

    assert (misses + hits == total)

    print(f"Hits: {hits} ({hits*100/total:.1f}%)")
    print(f"Perfect hits:{counts[0]} ({counts[0]*100/total:.1f}%)")
    print(f"Misses: {misses} ({misses*100/total:.1f}%)")


main()
