# atlas-df: a dataframe-oriented interface to RIPE Atlas

[![PyPI - License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/maxmouchet/atlas_df/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/badge/python-3-blue.svg?style=flat-square)](#)

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

## Development

```bash
git clone https://github.com/maxmouchet/atlas_df.git
cd atlas_df
pip install -e .
```

### Running tests

```bash
pip install -U pytest
TODO
```

## Maintainers

[@maxmouchet](https://github.com/maxmouchet)

## Contribute

PRs accepted.

## License

MIT © 2018 Maxime Mouchet
