from json import loads, dumps

# from RangeEncoder import RangeEncoder
from ansCoder import AnsCoder

from arguments import doArgs
from utils import buildSymTableRanges


precision = 16


"""
def buildSymTableRanges(symbols: list[int]) -> (list[int], list[int]):
    # Build a historgram of symbols.
    # Returns an array of symbols and counts sorted on frequency

    table = {}

    for sym in symbols:
        table[sym] = table.get(sym, 0) + 1

    syms, counts = zip(
            *sorted(table.items(), key=lambda x: x[1], reverse=True)
            )

    return syms, counts
"""


def rangeEncode(msg: list[int], inx_to_sym: list[int], counts: list[int],
                precision: int) -> (list[int], int):

    # Build range widths from counts and precision
    top = sum(counts)
    widths = [int((v << precision) / top) for v in counts]

    # Transform message symbols to range table indexes
    sym_to_inx = dict(zip(inx_to_sym, range(len(inx_to_sym))))
    indexes = [sym_to_inx[x] for x in msg]

    enc = AnsCoder(precision)

    # push indexes in reverse order because of stack semantics
    for i in reversed(indexes):
        enc.push(i,  widths)

    return enc.get_compressed(), len(enc)


def main() -> None:
    args = doArgs("Range encode (json->json)")

    json = loads(args.infile.read())

    token_tupples: list[int] = json["tokenList"]

    # Build message list where symbols are negative numbers for
    # indexes and possitive for unindedex tokens
    msg = [t if i == -1 else -1-i for (t, i, p) in token_tupples]

    inx_to_sym, counts = buildSymTableRanges(msg)

    compressed, length = rangeEncode(msg, inx_to_sym, counts, args.precision)

    del json["tokenList"]

    json.update({
        "precision": args.precision,
        "length": length,
        "inxToSym": inx_to_sym,
        "counts": counts,
        "compressed": compressed,
        })

    args.outfile.write(dumps(json).encode("latin-1"))


if __name__ == "__main__":
    main()
