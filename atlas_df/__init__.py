import logging

__name__ = 'atlas_df'

CACHE_DIR = '.atlas_df'
CACHE_ENABLED = True

API_SERVER = 'atlas.ripe.net'
FTP_SERVER = 'ftp.ripe.net'
# FTP_BASE_URL = 'https://ftp.ripe.net/ripe/atlas'

logging.getLogger(__name__).addHandler(logging.NullHandler())