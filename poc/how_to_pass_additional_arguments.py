# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(prog="pgr")

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    print(args)
    print(unknown)
