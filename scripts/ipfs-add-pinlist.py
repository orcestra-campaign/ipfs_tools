#!/usr/bin/env python3
import argparse
import subprocess
from functools import partial

import fsspec
import yaml


def get_pinlist(urlpath):
    with fsspec.open(urlpath, "r") as fp:
        return yaml.safe_load(fp.read())


def add_pins(pinlist):
    for pin in pinlist:
        cid = pin["cid"]

        if (name := pin.get("name")) is not None:
            subprocess.run(["ipfs", "pin", "add", "-r", cid, "-n", name])
        else:
            subprocess.run(["ipfs", "pin", "add", "-r", cid])


def _tag_filter(tag, pin):
    try:
        return tag in pin["meta"]["tags"]
    except KeyError:
        return False


def _main():
    parser = argparse.ArgumentParser(prog="add_pins")
    parser.add_argument("--pinlist", "-p", type=str, default="pinlist.yaml")
    parser.add_argument(
        "--tag", "-t", type=str, default=None, help="Only pin CIDs with given tag"
    )

    args = parser.parse_args()

    pinlist = get_pinlist(args.pinlist)

    if args.tag is not None:
        add_pins(filter(partial(_tag_filter, args.tag), pinlist))
    else:
        add_pins(pinlist)


if __name__ == "__main__":
    _main()
