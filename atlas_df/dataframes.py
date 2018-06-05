import re
from pandas import DataFrame, Series
from geopandas import GeoDataFrame, GeoSeries
from ripe.atlas.cousteau import AnchorRequest, MeasurementRequest
from .io import load_or_fetch_list
from .helpers import transform_df
from .parsers import parse_ip_address, parse_geometry, parse_timestamp

## Anchors


class AnchorDataFrame(DataFrame):
    @property
    def _constructor_sliced(self):
        return AnchorSeries

    def __init__(self, filters={}):
        lst = load_or_fetch_list(AnchorRequest, filters)
        super().__init__(lst)

        transform_df(
            self, {
                'apply': [('ip_v4', parse_ip_address),
                          ('ip_v6', parse_ip_address),
                          ('geometry', parse_geometry)],
                'index':
                'id'
            })


class AnchorGeoDataFrame(GeoDataFrame):
    @property
    def _constructor_sliced(self):
        return AnchorSeries

    def __init__(self, filters={}):
        lst = load_or_fetch_list(AnchorRequest, filters)
        super().__init__(lst)

        transform_df(
            self, {
                'apply': [('ip_v4', parse_ip_address),
                          ('ip_v6', parse_ip_address),
                          ('geometry', parse_geometry)],
                'index':
                'id',
                'geometry':
                'geometry'
            })


class AnchorSeries(Series):
    def fetch_mesh_measurements(self, filters={}):
        filters['description__startswith'] = 'Anchoring Mesh Measurement'
        filters['target'] = self['fqdn']
        return MeasurementDataFrame(filters)


## Measurements


class MeasurementDataFrame(DataFrame):
    @property
    def _constructor_sliced(self):
        return MeasurementSeries

    def __init__(self, filters):
        lst = load_or_fetch_list(MeasurementRequest, filters)
        super().__init__(lst)

        transform_df(
            self, {
                'apply':
                [('creation_time', parse_timestamp),
                 ('start_time', parse_timestamp),
                 ('status', 'status_id', lambda x: x['id']),
                 ('description', 'target_fqdn',
                  lambda x: re.match(r'.+for anchor\s+(.+)', x).group(1)),
                 ('status', lambda x: x['name'])],
                'index':
                'id'
            })


class MeasurementSeries(Series):
    def fetch_results(self, start_datetime, stop_datetime):
        pass
