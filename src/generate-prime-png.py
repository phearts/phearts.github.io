#!/usr/bin/env python3
from struct import pack, unpack
from zlib import crc32
from itertools import count
from pathlib import Path
from time import monotonic as now
from sympy import isprime


def primise(data: bytes):
    i, chunks = 8, [data[:8]]
    while i < len(data):
        length = unpack(">I", data[i: i + 4])[0]
        chunks.append(data[i: i + length + 12])
        i += length + 12
    prefix = b"".join(chunks[:2])
    suffix = b"".join(chunks[2:])
    r3 = (sum(prefix) + sum(suffix)) % 3
    r5 = (sum(prefix) + sum(suffix)) % 5
    for x in count():
        ignr_data = x.to_bytes((x.bit_length() + 7) // 8, "little")
        ignr = (
            pack(">I4s", len(ignr_data), b"igNr")
            + ignr_data
            + pack(">I", crc32(b"igNr" + ignr_data))
        )
        if (sum(ignr) + r3) % 3 == 0 or (sum(ignr) + r5) % 5 == 0:
            continue
        candidate = prefix + ignr + suffix
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
