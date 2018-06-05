import atlas_df
from atlas_df.io import load_or_fetch, load_or_fetch_list

def test_load_or_fetch(tmpdir):
    atlas_df.CACHE_DIR = tmpdir
    atlas_df.CACHE_ENABLED = True
    def dummy_fn(obj):
        return obj
    obj = {'some': 'data'}
    res = load_or_fetch(dummy_fn, {'obj': obj})
    assert res == obj

def test_load_or_fetch_list(tmpdir):
    atlas_df.CACHE_DIR = tmpdir
    atlas_df.CACHE_ENABLED = True
    def dummy_fn(obj):
        return obj
    obj = [{'some': 'data'}]
    res = load_or_fetch_list(dummy_fn, {'obj': obj})
    assert res == obj
