#!/usr/bin/env python3
import argparse
import subprocess

import yaml
import fsspec


def get_tree(urlpath):
    with fsspec.open(urlpath, "r") as fp:
        return yaml.safe_load(fp.read())


def write_folder(node, path):
    subprocess.run(["ipfs", "files", "mkdir", path])
    if isinstance(node, dict):
        for name, sub in node.items():
            write(sub, f"{path}/{name}")


def write_cid(cid, path):
    subprocess.run(["ipfs", "files", "cp", f"/ipfs/{cid}", path])


def write(node, path):
    if isinstance(node, str):
        return write_cid(node, path)
    elif node is None or isinstance(node, dict):
        return write_folder(node, path)


def get_mfs_cid(path):
    res = subprocess.run(["ipfs", "files", "stat", path, "--hash"], capture_output=True, text=True)
    return res.stdout.strip()


def main():
    parser = argparse.ArgumentParser(prog="write tree to IPFS")
    parser.add_argument("--tree", "-t", type=str, default="tree.yaml")
    parser.add_argument("--prefix", "-p", type=str, default="/ORCESTRA", help="IPFS MFS prefix")

    args = parser.parse_args()

    tree = get_tree(args.tree)

    write(tree, args.prefix)
    print(get_mfs_cid(args.prefix))


if __name__ == "__main__":
    exit(main())
