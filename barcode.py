class ITFReader:
    _values = (1,2,4,7,0)
    def __init__(self, narrow: float, wide: float):
        self.narrow = narrow
        self.wide = wide
    def decode_number(self, b: list[bool]) -> int:
        assert len(b) == 5
        assert sum(b) == 2
        #n = sum((_b * v for v, _b in zip(self._values, b)))
        n= self._values[b.index(True)] + self._values[-(b[::-1].index(True)+1)]
        return n if n < 10 else 0

    def decode_block(self, b : list[bool]) -> int:
        assert len(b) == 10
        n1, n2 = b[::2], b[1::2]
        n1, n2 = self.decode_number(n1), self.decode_number(n2)
        return 10*n1+n2

    def decode_code(self, b : list[bool]) -> int:
        assert not len(b) % 10
        n = 0
        for i in range(0,len(b), 10):
            block = b[i:i+10]
            n *= 100
            n += self.decode_block(block)
        return n

    def read(self, dists : list[float]) -> int:
        d = [round(n/10)*10 for n in dists]
        assert all((n in (self.narrow, self.wide) for n in d))
        c = [True if n > 10 else False for n in d]
        return self.decode_code(c)
        print(d)

if __name__ == "__main__":
    r = ITFReader(10,20)
    #n = r.decode_number([True, False, False, False, True])
    #n = r.decode_code([False, False, False, True, True, False, False, False, True, True]*2)
    n = r.read([9.4, 8, 11, 21, 19.8, 10, 10, 10, 20, 20])
    print(n)