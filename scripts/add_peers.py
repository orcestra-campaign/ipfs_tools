#!/usr/bin/env python3
import argparse
import json
import subprocess

import yaml


def main():
    parser = argparse.ArgumentParser(prog="Add known peers to IPFS config")
    parser.add_argument("--file", "-f", type=str, default="known_peers.yaml")

    args = parser.parse_args()

    with open(args.file, "r") as fp:
        peers = yaml.safe_load(fp)

    peer_config = json.dumps(
        [{"ID": p["ID"], "Addrs": p.get("Addrs", [])} for p in peers]
    )
    subprocess.run(["ipfs", "config", "--json", "Peering.Peers", peer_config])


if __name__ == "__main__":
    exit(main())
