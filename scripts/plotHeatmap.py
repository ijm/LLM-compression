import numpy as np
import xml.etree.ElementTree as E
import matplotlib.cm as cm

from transformers import GPT2Tokenizer
from json import loads

from arguments import doArgs

cmap = cm.get_cmap('inferno')


def htmlCol(c: float) -> str:
    (r, g, b) = cmap(np.clip(c, 0, 1))[:3]
    return f"color:#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x};"


def fInx(i, p):
    return 1.0 if i == -1 else np.clip(i, 0, 16) / 16


def fProb(i, p):
    return 1.0 if i == -1 else 1. - np.sqrt(p)


def renderDiv(parent, token_tupples, color_fun, tokenizer):
    tcol = E.SubElement(parent, 'div', attrib={"class": "tcol"})

    for (t, i, p) in token_tupples:
        word = tokenizer.decode(t, skip_special_tokens=True)

        v = color_fun(i, p) * 0.5 + 0.5
        E.SubElement(tcol, 'span', attrib={"style": htmlCol(v)}).text = word


def main():
    args = doArgs("Generate HTML word-heat map")
    modelname = args.modelname or "gpt2"

    tokenizer = GPT2Tokenizer.from_pretrained(modelname)

    json = loads(args.infile.read())

    token_tupples: list[int] = json["tokenList"]

    html = E.Element('html', xmlns="http://www.w3.org/1999/xhtml")
    head = E.SubElement(html, 'head')
    title = E.SubElement(head, 'title')
    title.text = 'heat map'
    style = E.SubElement(head, 'style')
    style.text = """
* {
    Color : #fff;
    Background : #000;
}

.heading {
  font-size: larger;
}
.row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 90%;
}

.column {
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
  flex: 1;
}

.tcol {
  width: 95%;
}
"""
    body = E.SubElement(html, 'body')

    row = E.SubElement(body, 'div', attrib={"class": "row"})

    c1 = E.SubElement(row, 'div', attrib={"class": "column"})
    E.SubElement(c1, 'div', attrib={"class": "heading"}) \
        .text = "Colorized on Index Depth"
    renderDiv(c1, token_tupples, fInx, tokenizer)

    c2 = E.SubElement(row, 'div', attrib={"class": "column"})
    E.SubElement(c2, 'div', attrib={"class": "heading"}) \
        .text = "Colorized on Model Probability"
    renderDiv(c2, token_tupples, fProb, tokenizer)

    str = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
        E.tostring(html, encoding='unicode', method='xml')

    args.outfile.write(str.encode("utf8"))


main()
