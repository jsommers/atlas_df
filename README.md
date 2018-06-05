# atlas-df: a dataframe-oriented interface to the RIPE Atlas API

![PyPI - License](https://img.shields.io/pypi/l/atlas_df.svg?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/atlas_df.svg?style=flat-square)



TODO: Fill out this long description.

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

## Development

```bash
git clone https://github.com/maxmouchet/atlas_df.git
cd atlas_df
pip install -e .
```

## Maintainers

[@maxmouchet](https://github.com/maxmouchet)

## Contribute

PRs accepted.

## License

MIT © 2018 Maxime Mouchet
