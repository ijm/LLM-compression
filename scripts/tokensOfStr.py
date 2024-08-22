from torch import set_num_threads
from transformers import AutoTokenizer
from json import dumps

from arguments import doArgs


def main():
    args = doArgs("Text to IR Token List")

    if args.numthread:
        set_num_threads(args.numthread)

    modelname = args.modelname or "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(modelname)

    text = args.infile.read().decode("utf8")
    tokens = tokenizer.encode(text, return_tensors="np")

    count = args.count or tokens.shape[1]

    json = {
        "modelName": modelname,
        "vocabSize": tokenizer.vocab_size,
        "comment": args.comment,
        "tokenList": [(int(x), -1, 0) for x in tokens[0, :count]]
        }

    args.outfile.write(dumps(json).encode("latin-1"))


if __name__ == "__main__":
    main()
