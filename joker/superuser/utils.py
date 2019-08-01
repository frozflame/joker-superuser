#!/usr/bin/env python3
# coding: utf-8
from functools import wraps


def under_asset_dir(*paths):
    import joker.superuser
    from joker.default import under_package_dir
    return under_package_dir(joker.superuser, 'asset', *paths)


def under_joker_superuser_dir(*paths):
    from joker.default import under_joker_dir
    return under_joker_dir('superuser', *paths)


def make_joker_superuser_dir(*paths):
    from joker.default import make_joker_dir
    return make_joker_dir('superuser', *paths)


def silent_function(func):
    """Do not report any error"""

    @wraps(func)
    def sfunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException:
            pass

    return sfunc
