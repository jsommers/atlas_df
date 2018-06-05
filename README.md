# atlas_df
 A dataframe-oriented API for RIPE Atlas data.

![PyPI - License](https://img.shields.io/pypi/l/atlas_df.svg?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/atlas_df.svg?style=flat-square)

```bash
pip install atlas_df
# or (dev)
pip install -e .
```

```python
import geopandas as gpd
from atlas_df.dataframes import AnchorGeoDataFrame

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
base = world.plot(color='white', edgecolor='black')

anchors.plot('is_ipv4_only', ax=base)
```

Class | Superclass | Index | Transformations
------|------------|-------|----------------
AnchorDataFrame | pandas.DataFrame | `id` | Build objects for `ip_v4`, `ip_v6`, `geometry`
AnchorGeoDataFrame | pandas.GeoDataFrame | `id` | Build objects for `ip_v4`, `ip_v6`, `geometry`
MeasurementDataFrame | pandas.DataFrame | `id` | Build objects for `creation_time`, `start_time`. Extract `status`, `status_id`, `target_fqdn`
