import re, math, logging
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

    @classmethod
    def from_api(cls, filters={}):
        """Fetch anchors list from Atlas API.

        Args:
            filters (dict): TODO.

        Returns:
            AnchorDataFrame
        """
        df = cls(load_or_fetch_list(AnchorRequest, filters))
        transform_df(
            df, {
                'apply': [('as_v4', lambda x: int(x) if not math.isnan(x) else nan),
                          ('as_v6', lambda x: int(x) if not math.isnan(x) else nan),
                          ('ip_v4', parse_ip_address),
                          ('ip_v6', parse_ip_address),
                          ('geometry', parse_geometry)],
                'index': 'id'
            }) # yapf: disable
        return df


# class AnchorGeoDataFrame(GeoDataFrame):
#     @property
#     def _constructor(self):
#         return AnchorGeoDataFrame

#     @propert
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
        """Fetch measurements list for the current anchor from Atlas API.

        Args:
            filters (dict): TODO.

        Returns:
            MeasurementDataFrame.
        """
        filters['description__startswith'] = 'Anchoring Mesh Measurement'
        filters['target'] = self['fqdn']
        return MeasurementDataFrame.from_api(filters)


## Probes

class ProbeDataFrame(DataFrame):
    @property
    def _constructor(self):
        return ProbeDataFrame

    @property
    def _constructor_sliced(self):
        return ProbeSeries

    @classmethod
    def from_api(cls, filters):
        """Fetch probes list from Atlas API.

        Args:
            filters (dict): TODO.

        Returns:
            ProbeDataFrame
        """
        raise NotImplementedError()

    @classmethod
    def from_ftp(cls): # TODO: Arg for file ?
        """Fetch probes list from Atlas FTP.

        Returns:
            ProbeDataFrame
        """
        raise NotImplementedError()


class ProbeSeries(Series):
    pass


## Measurements

class MeasurementDataFrame(DataFrame):
    @property
    def _constructor(self):
        return MeasurementDataFrame

    @property
    def _constructor_sliced(self):
        return MeasurementSeries

    @classmethod
    def from_api(cls, filters={}):
        """Fetch measurements list from Atlas API.

        Args:
            filters (dict): TODO.

        Returns:
            MeasurementDataFrame
        """
        if filters == {}:
            logging.getLogger(__name__).warning('No filters specified. This will be slow.')

        df = cls(load_or_fetch_list(MeasurementRequest, filters))
        transform_df(
            df, {
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
        return df


class MeasurementSeries(Series):
    def fetch_results(self, filters={}):
        """Fetch results for the current measurement from Atlas API.

        Args:
            filters (dict): TODO.

        Returns:
            MeasurementResultDataFrame
        """
        filters['msm_id'] = int(self.name)
        return MeasurementResultDataFrame.from_api(filters)


## Results


class MeasurementResultDataFrame(DataFrame):
    @property
    def _constructor(self):
        return MeasurementResultDataFrame

    @property
    def _constructor_sliced(self):
        return MeasurementResultSeries

    @classmethod
    def from_api(cls, filters={}):
        """Fetch results from Atlas API.

        Args:
            filters (dict): TODO.

        Returns:
            MeasurementResultDataFrame
        """
        if filters == {}:
            logging.getLogger(__name__).warning('No filters specified. This will be slow.')

        print(filters)
        df = cls(load_or_fetch(lambda **x: AtlasResultsRequest(**x).create()[1], filters))

        if len(df['type'].unique()) > 1:
            print('Warning: more than 1 measurement type in results')
        t = df['type'].unique()[0]

        if t == 'ping':
            transform_df(
                df, {
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
                df, {
                    'apply': [('timestamp', parse_timestamp),
                              ('stored_timestamp', parse_timestamp),
                              ('dst_addr', parse_ip_address),
                              ('src_addr', parse_ip_address)],
                    'index': ['prb_id', 'timestamp']
                }) # yapf: disable

        else:
            raise NotImplementedError('MeasurementResultDataFrame not implemented for %s' % t)

        return df


class MeasurementResultSeries(Series):
    pass