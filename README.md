# atlas-df: a dataframe-oriented interface to RIPE Atlas

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/maxmouchet/atlas_df/blob/master/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3-blue.svg?style=flat)](#)
[![Build Status](https://travis-ci.org/maxmouchet/atlas_df.svg?branch=master)](https://travis-ci.org/maxmouchet/atlas_df)
[![Coverage Status](https://coveralls.io/repos/github/maxmouchet/atlas_df/badge.svg?branch=master)](https://coveralls.io/github/maxmouchet/atlas_df?branch=master)

**Features:**
- [Caching](#cache) of API requests.
- geo plot/queries ...
TODO: logging

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Development](#development)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Install

```bash
pip install atlas_df
```

## Usage

```python
from atlas_df.dataframes import AnchorDataFrame

anchors = AnchorDataFrame()
measurements = anchors.loc[1029].fetch_mesh_measurements()
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
