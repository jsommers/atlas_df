import pandas as pd

import atlas_df
from atlas_df.dataframes import AnchorDataFrame, AnchorSeries # AnchorGeoDataFrame


def test_anchors_indexing_type():
    anchors = AnchorDataFrame()
    anchor = anchors[anchors.fqdn == anchors.fqdn.values[0]].iloc[0]
    assert type(anchor) == AnchorSeries


def test_anchors_concat_type():
    anchors = AnchorDataFrame()
    anchors_concat = pd.concat([anchors, anchors])
    assert type(anchors_concat) == AnchorDataFrame


# def test_geoanchors_indexing_type():
#     anchors = AnchorGeoDataFrame()
#     anchor = anchors[anchors.fqdn == anchors.fqdn.values[0]].iloc[0]
#     assert type(anchor) == AnchorSeries


# def test_geoanchors_concat_type():
#     anchors = AnchorGeoDataFrame()
#     anchors_concat = pd.concat([anchors, anchors])
#     assert type(anchors_concat) == AnchorGeoDataFrame
