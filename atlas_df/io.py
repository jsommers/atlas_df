import atlas_df
import os
import json


def fetch(fn, kwargs):
    return fn(**kwargs)


def load(fn, kwargs, salt):
    _fname = get_cache_fname(fn, kwargs, salt)
    with open(_fname, 'r') as f:
        res = json.load(f)
    return res


def store(fn, kwargs, salt, res):
    _fname = get_cache_fname(fn, kwargs, salt)

    try:
        os.mkdir(atlas_df.CACHE_DIR)
    except FileExistsError:
        pass

    with open(_fname, 'w') as f:
        json.dump(res, f)


def get_cache_fname(fn, kwargs, salt):
    # TODO: Fix fn.__name__ -> lambda
    _hash = hash((fn.__name__, salt, json.dumps(dict_to_str_kv(kwargs), sort_keys=True)))
    _fname = os.path.join(atlas_df.CACHE_DIR, '%s.json' % _hash)
    return _fname


def load_or_fetch(fn, kwargs={}, salt=None):
    if not atlas_df.CACHE_ENABLED:
        return fetch(fn, kwargs)

    try:
        res = load(fn, kwargs, salt)
    except (FileNotFoundError, json.JSONDecodeError):
        res = fetch(fn, kwargs)
        store(fn, kwargs, salt, res)

    return res


def load_or_fetch_list(fn, kwargs={}, salt=None):
    return load_or_fetch(lambda **x: list(fn(**x)), kwargs, salt)


# OPTIMIZE
def dict_to_str_kv(d):
    _d = d.copy()
    for k in _d:
        _d[k] = str(_d[k])
    return _d
