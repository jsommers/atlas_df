# atlas_df
 A dataframe-oriented API for RIPE Atlas data.

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