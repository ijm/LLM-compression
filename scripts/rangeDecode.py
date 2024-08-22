from json import loads, dumps

# from RangeEncoder import RangeEncoder
from ansCoder import AnsCoder

from arguments import doArgs


def rangeDecode(compressed: list[int], inx_to_sym: list[int],
                counts: list[int], length: int,  precision: int):

    # Build range widths from counts and precision
    top = sum(counts)
    widths = [int((v << precision) / top) for v in counts]

    enc = AnsCoder(precision, compressed=compressed, length=length)

    # Pop indexes and transform to symbols in a message list.
    msg = [inx_to_sym[enc.pop(widths)] for _ in range(length)]

    return msg


def main():
    args = doArgs("Range encode (json->json)")

    json = loads(args.infile.read())

    precision: int = json["precision"]
    length: int = json["length"]
    counts: list[int] = json["counts"]
    inx_to_sym: list[int] = json["inxToSym"]
    compressed: list[int] = json["compressed"]

    msg = rangeDecode(compressed, inx_to_sym, counts, length, precision)

    # Build token list where negative number map back to indexes.
    token_tupples = [(m, -1, 0.) if m >= 0 else (0, -1-m, 0.) for m in msg]

    json.update({
            "tokenList": token_tupples,
            })

    args.outfile.write(dumps(json).encode("latin-1"))


if __name__ == "__main__":
    main()
