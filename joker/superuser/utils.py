#!/usr/bin/env python3
# coding: utf-8


def under_templates_dir(*paths):
    import joker.superuser
    from joker.default import under_package_dir
    return under_package_dir(joker.superuser, 'templates', *paths)


