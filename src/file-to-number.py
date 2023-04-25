#!/usr/bin/env python3
import sys
from pathlib import Path

sys.set_int_max_str_digits(2**31 - 1)


def main(args):
    for path in map(Path, args):
        data = path.read_bytes()
        number = int.from_bytes(data, "little")
        print(f"{path} : {number}")


if __name__ == "__main__":
    main(sys.argv[1:])
