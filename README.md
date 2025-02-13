# ORCESTRA IPFS Tools

This repository contains tools which help working with [IPFS](https://ipfs.tech) that was collected during the ORCESTRA field campaign.

## Pinlist

The file `pinlist.yaml` contains a list of Pin objects according to the [IPFS Pinning Serices API Spec](https://ipfs.github.io/pinning-services-api-spec/):

![Pin Object](images/pin.png)

The pinlist contains descriptions of CIDs which are relevant for the field campaign and should be kept. The pinlist is used by pinning services to pin those CIDs.

The only required attribute is the `cid`, however, the other attributes are recommended. `name` and `meta` help identifying the Pin object. For incremental changes, The `meta.prev` attribute should point to an existing CID that the changes are based on. This allows IPFS to only fetch and pin differences, which can speed up retrieval.

It may be necessary to pin only subsets of all CIDs depending on available storage space or network bandwidth. In order to facilitate this selection, it is recommended to provide a list of `tags` within the Pin object metadata, e.g.:


```
cid: Qmas...
name: ORCESTRA HEAD v42
meta:
  tags: [all]
```

Currently known `tags` are:

* `all`: For "head" CIDs pointing to the whole ORCESTRA dataset
* `aux`: For auxiliary data that should be available on processing sites, but is not part of the ORCESTRA dataset

### Pinning the list

A very simple way to pin everything contained in the pinlist would be using [yq](https://mikefarah.gitbook.io/yq):

```bash
cat pinlist.yaml | yq .[].cid | xargs ipfs pin add -r
```

A simple way to e.g pin only dropsonde data could be:

```bash
cat pinlist.yaml | yq '.[] | select(.meta.tags.[] == "dropsonde").cid' | xargs ipfs pin add -r
```

## HEAD CIDs

The most common entry in the pinlist is the so-called "HEAD CID", which is a recursive pin pointing to the entire ORCESTRA dataset.
This CID is intended for easy mirroring of the whole dataset at different locations (e.g. DKRZ in Germany, CIMH in Barbados).

The HEAD CID can be created by writing the whole dataset tree to the [Mutable File System](https://docs.ipfs.tech/concepts/file-systems/#mutable-file-system-mfs) (MFS).
The structure of the dataset tree and the associated CIDs are defined by the `tree.yaml` file.
The convenience script `scripts/write_tree.py` can be used to write the tree currently described in `tree.yaml` to the MFS and retrieve the HEAD CID.

## Asynchronous pinning

One caveat of the current Pull Request (PR) based pinning system is the need for synchronicity between the merging of a new dataset and the availability of that data.
This means that the data is initially only available on the system of the data provider who has opened a PR to add their data.
In order to merge that PR, the data must be available, i.e. the data provider's system must be reachable.
This is likely to be the case for servers or HPC systems, but less likely for personal computers of virtual machines.

A possible workaround is to create Content Addressable Archives (CAR).
These archives bundle the (recursive) CIDs together with the data.
You can create a CAR for a given CID by running

```sh
ipfs dag export <CID> > <CID>.car
```

The resulting CAR can then be made available when opening a PR (e.g. on the Levante file system or via a file sharing provider, depending on size).
The CAR can then also be used to pin the data if the data provider's system is unreachable.
