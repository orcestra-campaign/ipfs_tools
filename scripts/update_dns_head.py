import os
import json
import requests


def get_config_dir():
    if "ORCESTRA_CONFIG" in os.environ:
        return os.path.join(os.environ["ORCESTRA_CONFIG"])
    elif "XDG_CONFIG_PATH" in os.environ:
        return os.path.join(os.environ["XDG_CONFIG_HOME"], "orcestra")
    elif "HOME" in os.environ:
        return os.path.join(os.environ["HOME"], ".config", "orcestra")
    else:
        raise RuntimeError("could not find config path")


class DNSApi:
    def __init__(self):
        config_dir = get_config_dir()
        with open(os.path.join(config_dir, "data_dns.json")) as configfile:
            config = json.load(configfile)
        prefix = config["prefix"]
        secret = config["secret"]

        self.headers = {
            "X-API-Key": f"{prefix}.{secret}",
            "Content-Type": "application/json",
        }

        self.zone_id = "d2e2d4cc-67bf-11ef-b510-0a586444315f"
        self.base_url = "https://api.hosting.ionos.com/dns/v1/"

    def _url(self, path):
        return self.base_url + path

    def get_records(self):
        res = requests.get(self._url(f"zones/{self.zone_id}"), headers=self.headers)
        res.raise_for_status()
        return res.json()["records"]

    def update_dnslink(self, ipfs_link, subdomain="head", ttl=300):
        data = [
            {
                "name": f"_dnslink.{subdomain}.orcestra-data.org",
                "type": "TXT",
                "content": f"dnslink={ipfs_link}",
                "ttl": ttl,
                "priority": 0,
            }
        ]

        res = requests.patch(
            self._url(f"zones/{self.zone_id}"), headers=self.headers, json=data
        )
        res.raise_for_status()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ipfs_link", help="IPFS link, e.g.: /ipfs/CID")
    args = parser.parse_args()

    api = DNSApi()

    api.update_dnslink(args.ipfs_link)


if __name__ == "__main__":
    exit(main())
