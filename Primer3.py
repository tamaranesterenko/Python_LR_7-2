# !/usr/bin/env python3
# -*- cosing: utf-8 -*-

import pathlib


def unique_path(directory, name_pattern):
    counter = 0
    while True:
        counter += 1
        path = directory/name_pattern.format(counter)
        if not path.exists():
            return path

