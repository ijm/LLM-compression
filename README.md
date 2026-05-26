# LLM-compression

Supporting code for [*A Compression View of LLMs*](https://ghost.codenamejimmy.com/a-compression-view-of-large-language-models/). See [article.md](article.md) for the full argument.

The code consists of eight small scripts wired in a pipe: an LLM predicts the next token, the surprises are ANS-encoded, and you can run it backward to decompress or to make up text by supplying correction bytes on stdin instead of a `.bin` file. This is not meant for real compression work.

Needs Python 3.9+, PyTorch, `transformers`, NumPy, Matplotlib ([requirements.txt](requirements.txt)). The first run downloads weights from Hugging Face.

## Running the article examples

Same layout as the article. Default model is `gpt2`; use `-n` for another Hugging Face causal LM.

The `run.sh` scripts put `scripts` on `PYTHONPATH`. From the repo root, `python3 -m scripts.tokensOfStr` etc. also works.

### Compress / decompress

Opening of *A Study in Scarlet* in `examples/compressor/`.

```bash
cd examples/compressor
./run.sh AStudyInScarlet.txt
```

Writes `AStudyInScarlet.bin`, files under `AStudyInScarlet/`, and `AStudyInScarlet.decomp.txt` to check lossless round-trip. `modelToInx` and `modelOfInx` are slow: one forward pass per token. The size table in the article uses `AStudyInScarlet2.txt` (same text, second copy in the tree).

Gzip baseline with the period case-flip trick: [examples/gzipFilp](examples/gzipFilp/).

### Generation

"Generating Some Text" in the article. Prompt on `-c`, corrections from stdin. All zeros means always take the model's first choice in the top-k list:

```bash
cd examples/generate
./run.sh
```

### Plots

Run the compressor example first, then:

```bash
cd figures/symbolHist && ./run.sh
cd figures/heatmap && ./run.sh
```

Both read `examples/compressor/AStudyInScarlet/AStudyInScarlet.ttout.json` (figures 4 and 5 in the article).

## Scripts

Compression: `tokensOfStr.py`, `modelToInx.py`, `rangeEncode.py`, `binOfRange.py`

Decompression: `binToRange.py`, `rangeDecode.py`, `modelOfInx.py`, `tokensToStr.py`

`tokensOfData.py` is only for the generation demo. Stages speak JSON on purpose so you can poke at or plot the intermediates.

## File sizes

The article quotes gpt2 on the Scarlet excerpt: `.bin` about 25% of raw `.txt`, `gzip -9` about 39%. The `.bin` does not include the model weights. Phi-2 should do better; re-run `./run.sh` after changing `model.sh` and compare your `*.bin` size.

## License

[LICENSE](LICENSE)
