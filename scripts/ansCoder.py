class AnsCoder:
    def __init__(self, precision: int, compressed: list = [], length: int = 0):
        self.length = length
        self.precision = precision
        self.mask = (1 << precision) - 1  # (a string of precision one-bits)
        self.bulk = compressed.copy()  # (We will mutate bulk below.)
        self.head = 0
        # Establish invariant (ii):
        while len(self.bulk) != 0 and (self.head >> precision) == 0:
            self.head = (self.head << precision) | self.bulk.pop()

    def __len__(self) -> int:
        return self.length

    def push(self, symbol: int, m: list[int]) -> None:  # Encodes one symbol.
        # Check if encoding directly onto head would violate invariant (i):
        if (self.head >> self.precision) >= m[symbol]:
            # Transfer one word of compressed data from head to bulk:
            self.bulk.append(self.head & self.mask)  # (“&” is bitwise and)
            self.head >>= self.precision
            # At this point, invariant (ii) is definitely violated,
            # but the operations below will restore it.

        z = self.head % m[symbol] + sum(m[0:symbol])
        self.head //= m[symbol]
        self.head = (self.head << self.precision) | z  # (This is
        # equivalent to “self.head * n + z”, just slightly faster.)
        self.length += 1

    def pop(self, m: list[int]) -> int:  # Decodes one symbol.
        z = self.head & self.mask  # (same as “self.head % n” but faster)
        self.head >>= self.precision  # (same as “//= n” but faster)
        for symbol, m_symbol in enumerate(m):
            if z >= m_symbol:
                z -= m_symbol
            else:
                break  # We found the symbol that satisfies z ∈ Zi(symbol).
        self.head = self.head * m_symbol + z
        self.length -= 1

        # Restore invariant (ii) if it is violated (which happens exactly
        # if the encoder transferred data from head to bulk at this point):
        if (self.head >> self.precision) == 0 and len(self.bulk) != 0:
            # Transfer data back from bulk to head (“|” is bitwise or):
            self.head = (self.head << self.precision) | self.bulk.pop()

        return symbol

    def get_compressed(self) -> list[int]:
        compressed = self.bulk.copy()  # (We will mutate compressed below.)
        head = self.head
        # Chop head into precision-sized words and append to compressed:
        while head != 0:
            compressed.append(head & self.mask)
            head >>= self.precision

        return compressed
