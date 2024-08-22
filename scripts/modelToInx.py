import numpy as np
import torch as T

from torch.nn.functional import softmax

from transformers import AutoModelForCausalLM
from json import loads, dumps
from sys import stderr
from time import sleep

from arguments import doArgs


def main():
    args = doArgs("Populate index and probabilities.")

    if args.numthread:
        T.set_num_threads(args.numthread)

    json = loads(args.infile.read())

    modelname = json["modelName"]

    if args.modelname and args.modelname != modelname:
        print("Warning model name does not match IR file.", file=stderr)

    model = AutoModelForCausalLM.from_pretrained(modelname)

    token_tupples = np.array(json["tokenList"])

    window = args.contextwindow
    topN = args.topN
    count = args.count or token_tupples.shape[0]

    probprecision = 1e6

    for p_end in range(1, count):
        p_start = max(0, p_end - window)

        with T.no_grad():
            token_predicts = model(T.tensor(
                token_tupples[p_start:p_end, 0:1].T))[0][0, -1, :]

        token_probabilities = softmax(token_predicts, dim=-1)

        best_inxs = T.topk(token_predicts, topN).indices.tolist()

        best_prob = token_probabilities[best_inxs].tolist()

        t = token_tupples[p_end, 0]
        try:
            i = best_inxs.index(t)
            token_tupples[p_end, 1] = i
            token_tupples[p_end, 2] = best_prob[i] * probprecision + 0.5
        except ValueError:
            pass
        print(p_end, token_tupples[p_end], file=stderr)
        sleep(args.cooldown)

    output = {
        "modelName": modelname,
        "vocabSize": json["vocabSize"],
        "comment": (json.get("comment") or "") + (args.comment or ""),
        "contextwindow": window,
        "topN": topN,
        "tokenList": [(int(t), int(i), float(p)/probprecision)
                      for (t, i, p) in token_tupples]
        }

    args.outfile.write(dumps(output).encode("latin-1"))


if __name__ == "__main__":
    main()
