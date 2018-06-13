import re
from numpy import nan
from pandas import DataFrame, Series
from geopandas import GeoDataFrame, GeoSeries
from ripe.atlas.cousteau import AtlasResultsRequest, AnchorRequest, MeasurementRequest
from .io import load_or_fetch, load_or_fetch_list
from .helpers import transform_df
from .parsers import parse_ip_address, parse_geometry, parse_timestamp

## Anchors


class AnchorDataFrame(DataFrame):
    @property
    def _constructor(self):
        return AnchorDataFrame

    @property
    def _constructor_sliced(self):
        return AnchorSeries

    def __init__(self, filters={}):
        if type(filters) is not dict:
            return super().__init__(filters)

        lst = load_or_fetch_list(AnchorRequest, filters)
        super().__init__(lst)

        transform_df(
            self, {
                'apply': [('ip_v4', parse_ip_address),
                          ('ip_v6', parse_ip_address),
                          ('geometry', parse_geometry)],
                'index': 'id'
            }) # yapf: disable


# class AnchorGeoDataFrame(GeoDataFrame):
#     @property
#     def _constructor(self):
#         return AnchorGeoDataFrame

#     @property
#     def _constructor_sliced(self):
#         return AnchorSeries

#     def __init__(self, filters={}):
#         if type(filters) is not dict:
#             return super().__init__(filters)

#         lst = load_or_fetch_list(AnchorRequest, filters)
#         super().__init__(lst)

#         transform_df(
#             self, {
#                 'apply': [('ip_v4', parse_ip_address),
#                           ('ip_v6', parse_ip_address),
#                           ('geometry', parse_geometry)],
#                 'index': 'id',
#                 'geometry': 'geometry'
#             }) # yapf: disable


class AnchorSeries(Series):
    def fetch_mesh_measurements(self, filters={}):
        filters['description__startswith'] = 'Anchoring Mesh Measurement'
        filters['target'] = self['fqdn']
        return MeasurementDataFrame(filters)


## Measurements


class MeasurementDataFrame(DataFrame):
    @property
    def _constructor(self):
        return MeasurementDataFrame

    @property
    def _constructor_sliced(self):
        return MeasurementSeries

    def __init__(self, filters):
        if type(filters) is not dict:
            return super().__init__(filters)

        lst = load_or_fetch_list(MeasurementRequest, filters)
        super().__init__(lst)

        transform_df(
            self, {
                'apply': [
                    ('creation_time', parse_timestamp),
                    ('start_time', parse_timestamp),
                    ('status', 'status_id', lambda x: x['id']),
                    #  ('description', 'target_fqdn',
                    #   lambda x: re.match(r'.+for anchor\s+(.+)', x).group(1)),
                    ('status', lambda x: x['name'])
                ],
                'index': 'id'
            }) # yapf: disable


class MeasurementSeries(Series):
    def fetch_results(self, filters={}):
        filters['msm_id'] = int(self.name)
        return MeasurementResultDataFrame(filters)


## Results


class MeasurementResultDataFrame(DataFrame):
    @property
    def _constructor(self):
        return MeasurementResultDataFrame

    @property
    def _constructor_sliced(self):
        return MeasurementResultSeries

    def __init__(self, filters):
        if type(filters) is not dict:
            return super().__init__(filters)

        lst = load_or_fetch(lambda **x: AtlasResultsRequest(**x).create()[1],
                            filters)
        super().__init__(lst)

        if len(self['type'].unique()) > 1:
            print('Warning: more than 1 measurement type in results')
        t = self['type'].unique()[0]

        if t == 'ping':
            transform_df(
                self, {
                    'apply': [('timestamp', parse_timestamp),
                              ('stored_timestamp', parse_timestamp),
                              ('dst_addr', parse_ip_address),
                              ('src_addr', parse_ip_address)],
                    'replace': [('avg', -1.0, nan),
                                ('min', -1.0, nan),
                                ('max', -1.0, nan)],
                    'index': ['prb_id', 'timestamp']
                }) # yapf: disable
        elif t == 'traceroute':
            transform_df(
                self, {
                    'apply': [('timestamp', parse_timestamp),
                              ('stored_timestamp', parse_timestamp),
                              ('dst_addr', parse_ip_address),
                              ('src_addr', parse_ip_address)],
                    'index': ['prb_id', 'timestamp']
                }) # yapf: disable

        else:
            print('MeasurementResultDataFrame not implemented for %s' % t)


class MeasurementResultSeries(Series):
    pass