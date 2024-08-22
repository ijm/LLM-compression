from torch import set_num_threads
from transformers import AutoTokenizer
from json import dumps

from arguments import doArgs


def main():
    args = doArgs("Text as data to Indicies Token List")

    if args.numthread:
        set_num_threads(args.numthread)

    modelname = args.modelname or "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(modelname)

    data = args.infile.read().decode("latin-1")
    inxs = []
    for a in data:
        inxs.append((0, ord(a) & 15, 0.))
        inxs.append((0, ord(a) >> 4, 0.))

    tokens = tokenizer.encode(args.comment, return_tensors="np")

    count = args.count or tokens.shape[1]

    json = {
        "modelName": modelname,
        "vocabSize": tokenizer.vocab_size,
        "comment": args.comment,
        "tokenList": [(int(x), -1, 0) for x in tokens[0, :count]] + inxs
    }

    args.outfile.write(dumps(json).encode("latin-1"))


if __name__ == "__main__":
    main()
