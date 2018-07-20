# atlas_df: a dataframe-oriented interface to RIPE Atlas

[![Python Version](https://img.shields.io/badge/python-3-blue.svg?style=flat)](#)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/maxmouchet/atlas_df/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/maxmouchet/atlas_df.svg?branch=master)](https://travis-ci.org/maxmouchet/atlas_df)
[![Documentation Status](https://readthedocs.org/projects/atlas_df/badge/?version=latest)](https://atlas-df.readthedocs.io/en/latest/)
[![Coverage Status](https://coveralls.io/repos/github/maxmouchet/atlas_df/badge.svg?branch=master)](https://coveralls.io/github/maxmouchet/atlas_df?branch=master)

[![Example Map](https://github.com/maxmouchet/atlas_df/blob/master/examples/1001_map.png)](#)

atlas_df is an interface to the RIPE Atlas API built on top of the official client ([ripe-atlas-cousteau](https://github.com/RIPE-NCC/ripe-atlas-cousteau)). It converts Atlas resources to [pandas](https://github.com/pandas-dev/pandas) and [geopandas](https://github.com/geopandas/geopandas) DataFrames/Series. This makes the use of the Python scientific ecosystem (matplotlib, seaborn, numpy, scikit-learn, ...) with Atlas data very easy.

**Features:**
- Conversion of RIPE Atlas resources to `DataFrame` and `Series` objects.
- [Caching](#cache) of API requests.
- geo plot/queries ...
TODO: logging, computation of geo distance between anchors/probes, ...

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Development](#development)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Install

atlas_df is a Python 3 library, depending on your setup, you may want to use `pip` or `pip3`.

```bash
pip install atlas_df
```

## Usage

A comprehensive (TODO) documentation is on [Read the Docs](https://atlas-df.readthedocs.io/en/latest/).

```python
from atlas_df.dataframes import AnchorDataFrame

anchors = AnchorDataFrame.from_api()
measurements = anchors.loc[1029].fetch_mesh_measurements()
```


### Anchoring

```python
import datetime as dt
from atlas_df.anchoring import AnchoringMesh

anchoring_mesh = AnchoringMesh()

anchor_fqdn_a = 'al-tia-as42409.anchors.atlas.ripe.net'
anchor_fqdn_b = 'nc-nou-as56055.anchors.atlas.ripe.net'
start_datetime = dt.datetime(2018, 5, 1)
stop_datetime  = dt.datetime(2018, 5, 7)
af = 4

traceroute_ab, traceroute_ba = anchoring_mesh.fetch_results(anchor_fqdn_a, anchor_fqdn_b, af, 'traceroute', {'start': START_DATETIME, 'stop': STOP_DATETIME})
```

### Cache

```python
import atlas_df
atlas_df.CACHE_DIR = '.atlas_df'
atlas_df.CACHE_ENABLED = True
```

## Development

```bash
git clone https://github.com/maxmouchet/atlas_df.git
cd atlas_df
pip install -e .
```

Code is formatted using [yapf](https://github.com/google/yapf).

### Building documentation

```bash
pip install sphinx sphinx-rtd-theme
sphinx-apidoc -f -o docs/source/ atlas_df
cd docs; make html
```

### Running tests

```bash
pip install -U pytest pytest-cov
py.test --cov=atlas_df tests/
```

## Maintainers

[@maxmouchet](https://github.com/maxmouchet)

## Contribute

PRs accepted.

## License

MIT © 2018 Maxime Mouchet
