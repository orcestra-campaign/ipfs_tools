import argparse
import yaml
import subprocess
from collections.abc import MutableMapping


def extract_values(dictionary):
    """Yield all **values** from a nested dictionary."""
    for value in dictionary.values():
        if isinstance(value, MutableMapping):
            yield from extract_values(value)
        else:
            yield value


def parse_yaml(yamlfile):
    """Open a YAML file and return the parsed content."""
    with open(yamlfile) as fp:
        return yaml.safe_load(fp)


def pin(cid):
    """Pin a given CID using IPFS."""
    subprocess.run(["ipfs", "pin", "add", "--progress", "-r", cid])


def _main():
    parser = argparse.ArgumentParser(description="Pin all CIDs from a tree YAML.")
    parser.add_argument("-f", "--filename", default="tree.yaml")
    args = parser.parse_args()

    cids = extract_values(parse_yaml(args.filename))
    list(map(pin, cids))


if __name__ == "__main__":
    _main()
