from json import dumps
from struct import unpack, unpack_from

from arguments import doArgs


def main():
    def fromByteArray(f: str, barr: bytearray, N: int, w: int) -> None:
        return [unpack_from(f, barr, i*w)[0] for i in range(N)]

    args = doArgs("Unpack Binary range encode data (bin->json)")

    buf = bytearray(4 * 5)
    args.infile.readinto(buf)

    l_inx_to_sym, l_counts, l_compressed, length, precision = \
        unpack("!IIIII", buf)

    b_inx_to_sym = bytearray(4 * l_inx_to_sym)
    b_counts = bytearray(4 * l_counts)
    b_compressed = bytearray(4 * l_compressed)

    args.infile.readinto(b_inx_to_sym)
    args.infile.readinto(b_counts)
    args.infile.readinto(b_compressed)

    # prep for json output. Adding back '1' counts back to end of counts array.
    output = {
        "precision": precision,
        "length": length,

        "inxToSym": fromByteArray("!i", b_inx_to_sym, l_inx_to_sym, 4),

        "counts": fromByteArray("!I", b_counts, l_counts, 4) +
        [1] * (l_inx_to_sym - l_counts),

        "compressed": fromByteArray("!I", b_compressed, l_compressed, 4),
    }

    args.outfile.write(dumps(output).encode("latin-1"))


main()
