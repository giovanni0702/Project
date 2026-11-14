#!/usr/bin/env python3
"""Download a city's source data through its adapter. Raw files stay out of git.
Usage: scripts/fetch_city.py <city_id>"""
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
adapter = importlib.import_module(f"cities.{sys.argv[1]}.adapter")
print("\n".join(adapter.fetch()))
