# ORCESTRA IPFS Tools

This repository contains tools which help working with [IPFS](https://ipfs.tech) that was collected during the ORCESTRA field campaign.

## Pinlist

The file `pinlist.yaml` contains a list of Pin objects according to the [IPFS Pinning Serices API Spec](https://ipfs.github.io/pinning-services-api-spec/):

![Pin Object](images/pin.png)

The pinlist contains descriptions of CIDs which are relevant for the field campaign and should be kept. The pinlist is used by pinning services to pin those CIDs.

The only required attribute is the `cid`, however, the other attributes are recommended. `name` and `meta` help identifying the Pin object. For incremental changes, The `meta.prev` attribute should point to an existing CID that the changes are based on. This allows IPFS to only fetch and pin differences, which can speed up retrieval.

It may be necessary to pin only subsets of all CIDs depending on available storage space or network bandwidth. In order to facilitate this selection, it is recommended to provide a list of `tags` within the Pin object metadata, e.g.:


```
cid: bafy...
name: Dropsonde data v1
meta:
  tags: [dropsonde]
```

Currently known `tags` are:

* `bahamas`: For BAHAMAS data
* `catalog`: For catalogs: they are important and should be quickly retrievable for everyone, but usually aren't very big in size.
* `dropsonde`: For dropsonde data
* `radiosonde`: For radiosonde data

### Pinning the list

A very simple way to pin everything contained in the pinlist would be using [yq](https://mikefarah.gitbook.io/yq):

```bash
cat pinlist.yaml | yq .[].cid | xargs ipfs pin add -r
```

A simple way to e.g pin only dropsonde data could be:

```bash
cat pinlist.yaml | yq '.[] | select(.meta.tags.[] == "dropsonde").cid' | xargs ipfs pin add -r
```
