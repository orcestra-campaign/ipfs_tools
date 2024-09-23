#!/usr/bin/env python3
import argparse
import json
import subprocess
from collections import defaultdict
from itertools import chain

import fsspec
import yaml


def get_ipfs_config():
    return json.loads(
        subprocess.run(["ipfs", "config", "show"], capture_output=True).stdout
    )


def main():
    parser = argparse.ArgumentParser(prog="Add known peers to IPFS config")
    parser.add_argument("--file", "-f", type=str, default="known_peers.yaml")

    args = parser.parse_args()

    ipfs_config = get_ipfs_config()

    with fsspec.open(args.file, "r") as fp:
        known_peers = yaml.safe_load(fp)

    peers = defaultdict(set)
    for peer in chain(ipfs_config["Peering"]["Peers"], known_peers):
        peers[peer["ID"]].update(peer.get("Addrs", []))

    peer_config = json.dumps([{"ID": i, "Addrs": list(a)} for i, a in peers.items()])
    subprocess.run(["ipfs", "config", "--json", "Peering.Peers", peer_config])


if __name__ == "__main__":
    exit(main())
