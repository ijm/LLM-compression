from json import loads

from arguments import doArgs


def main():
    args = doArgs("Stats from range encoded output json")
#    modelname = args.modelname or "gpt2"

#      tokenizer = GPT2Tokenizer.from_pretrained(modelname)

    json = loads(args.infile.read())

    length = json["length"]
    counts = json["counts"]
    inx_to_sym = json["inxToSym"]
    compressed = json["compressed"]

# Strip unnecessary '1' counts from the end of the counts array.
    counts = counts[0:counts.index(1)]

    l_counts = len(counts)
    l_inx_to_sym = len(inx_to_sym)
    l_compressed = len(compressed)

    wordlen = 4

    print(f"Total Symbols: {length} ({length*wordlen/1000:.01f} kBytes)")
    print(f"Size of counts table: {l_counts} "
          f"({l_counts*wordlen/1000:.01f} kBytes)")
    print(f"Size of symbol table: {l_inx_to_sym} "
          f"({l_inx_to_sym*wordlen/1000:.01f} kBytes)")
    print(f"Size of compressed output: {l_compressed} "
          f"({l_compressed*wordlen/1000:.01f} kBytes)")


main()
