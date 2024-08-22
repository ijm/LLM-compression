def buildSymTableRanges(symbols: list[int]) -> (list[int], list[int]):
    # Build a historgram of symbols.
    # Returns an array of symbols and counts sorted on frequency

    table = {}

    for sym in symbols:
        table[sym] = table.get(sym, 0) + 1

    syms, counts = zip(
            *sorted(table.items(), key=lambda x: x[1], reverse=True)
            )

    return syms, counts
