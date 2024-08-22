import numpy as np
import torch as T

from torch.nn.functional import softmax

from transformers import AutoModelForCausalLM
from json import loads, dumps
from sys import stderr
from time import sleep

from arguments import doArgs


def main():
    args = doArgs("Populate tokend and probabilities from indexes.")

    if args.numthread:
        T.set_num_threads(args.numthread)

    json = loads(args.infile.read())

    modelname = args.modelname

    model = AutoModelForCausalLM.from_pretrained(modelname)

    token_tupples = json["tokenList"]
    window = args.contextwindow
    topN = args.topN
    count = args.count or len(token_tupples)
    probprecision = 1e6

    token_tupples = np.array(json["tokenList"])
    token_tupples[:, 2] *= probprecision
    token_tupples = token_tupples.astype(int)

    window = args.contextwindow
    precision = 1e6

    for p_end in range(1, count):
        i = token_tupples[p_end, 1]
        p_start = max(0, p_end - window)
        if i != -1:

            with T.no_grad():
                ins = token_tupples[p_start:p_end, 0:1].T
                token_predicts = model(T.tensor(ins))[0][0, -1, :]

            token_probabilities = softmax(token_predicts, dim=-1)

            best_inxs = T.topk(token_predicts, topN).indices.tolist()

            best_prob = token_probabilities[best_inxs].tolist()

            token_tupples[p_end, 0] = best_inxs[i]
            token_tupples[p_end, 2] = best_prob[i] * precision + 0.5
            sleep(args.cooldown)

        print(p_end, token_tupples[p_end], file=stderr)

    json.update({
        "modelName": modelname,
        "contextwindow": window,
        "topN": topN,
        "tokenList": [(int(t), int(i), float(p)/precision)
                      for (t, i, p) in token_tupples]
        })

    args.outfile.write(dumps(json).encode("latin-1"))


if __name__ == "__main__":
    main()
