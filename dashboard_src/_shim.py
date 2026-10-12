# -*- coding: utf-8 -*-
"""Generator entry. The full template lives in gen.py; this shim exists so the
build workflow has a predictable entry point."""
import os, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gen import main_data_only as _unused  # noqa
