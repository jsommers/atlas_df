import json


def load_or_fetch(fn, kwargs={}, salt=None):
    _hash = hash((salt, json.dumps(kwargs, sort_keys=True)))
    _fname = '%s.json' % _hash

    # TODO: mkdir cache

    try:
        with open(_fname, 'r') as f:
            res = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        res = fn(**kwargs)
        with open(_fname, 'w') as f:
            json.dump(res, f)

    return res


def load_or_fetch_list(fn, kwargs={}, salt=None):
    return load_or_fetch(lambda **x: list(fn(**x)), kwargs, salt)
