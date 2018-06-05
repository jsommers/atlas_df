import datetime as dt
from shapely.geometry import Point
from ipaddress import ip_address, ip_network


def parse_ip_address(obj):
    if obj is None:
        return
    return ip_address(obj.strip())


def parse_ip_network(obj):
    if obj is None:
        return
    return ip_network(obj.strip())


def parse_geometry(obj):
    if obj is None:
        return
    # TODO: Check latitude/longitude ...
    return Point(obj['coordinates'])


def parse_timestamp(obj):
    if obj is None:
        return
    return dt.datetime.fromtimestamp(float(obj))