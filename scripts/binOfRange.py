from json import loads
from struct import pack, pack_into

from arguments import doArgs


def main() -> None:
    def toByteArray(f: str, arr: list[int], W: int) -> bytearray:
        barr = bytearray(4 * len(arr))

        for i, v in enumerate(arr):
            pack_into(f, barr, i * W, v)

        return barr

    args = doArgs("Binary pack range encode data (json->bin)")

    json = loads(args.infile.read())

    precision = json["precision"]
    length = json["length"]
    counts = json["counts"]
    inx_to_sym = json["inxToSym"]
    compressed = json["compressed"]

    # Strip unnecessary '1' counts from the end of the counts array.
    counts = counts[0:counts.index(1)]

    lens = pack("!IIIII", len(inx_to_sym), len(counts),
                len(compressed), length, precision)

    b_inx_to_sym = toByteArray("!i", inx_to_sym, 4)
    b_counts = toByteArray("!I", counts, 4)
    b_compressed = toByteArray("!I", compressed, 4)

    args.outfile.write(b"".join([lens, b_inx_to_sym, b_counts, b_compressed]))


main()
