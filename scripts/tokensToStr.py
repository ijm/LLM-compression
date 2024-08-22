from torch import set_num_threads, tensor
from transformers import AutoTokenizer
from json import loads

from arguments import doArgs


def main():
    args = doArgs("IR Token List to Text")

    if args.numthread:
        set_num_threads(args.numthread)

    tokenizer = AutoTokenizer.from_pretrained(args.modelname)

    json = loads(args.infile.read())

    token_tupples = json["tokenList"]

    (tokens, indxs, probs) = zip(*token_tupples)

    args.outfile.write(tokenizer.decode(tensor(tokens)).encode("utf8"))


if __name__ == "__main__":
    main()
