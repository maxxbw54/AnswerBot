# -*- coding: UTF-8 -*-

import os


def get_base_path():
    return os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    print get_base_path()