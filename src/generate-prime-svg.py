#!/usr/bin/env python3
from itertools import count
from pathlib import Path
from time import monotonic as now
from sympy import isprime


def primise(data: bytes):
    data = data.strip().replace(b"\n", b"") + b"\n"
    if data[0] % 2 == 0:
        data = b"\t" + data
    i = data.find(b'"', data.find(b'<rect width="') + 13)
    for x in count():
        candidate = data[:i] + str(x).encode() + data[i:]
        if isprime(int.from_bytes(candidate, "little")):
            return candidate


def main(args):
    for path in map(Path, args):
        data = path.read_bytes()
        print(f"Trying to find prime-number variant of {path}...")
        t0 = now()
        result_path = path.with_stem(f"{path.stem}-prime")
        result_path.write_bytes(primise(data))
        print(f"Found in {now()-t0:0.3f}s. Saved to {result_path}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
