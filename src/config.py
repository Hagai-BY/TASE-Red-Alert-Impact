"""
Config helpers for locating the data directory.
Priority: ENV["DATA_ROOT"] > data_config.yaml > ./data
"""
from __future__ import annotations
import os, yaml

def data_root() -> str:
    if "DATA_ROOT" in os.environ and os.environ["DATA_ROOT"]:
        return os.environ["DATA_ROOT"]
    try:
        with open("data_config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
            if "data_root" in cfg and cfg["data_root"]:
                return cfg["data_root"]
    except FileNotFoundError:
        pass
    return "./data"

def path(*parts: str) -> str:
    return os.path.join(data_root(), *parts)


def prefer_sample_path(filename_in_sample: str) -> str:
    """Return path to a file in data/sample if it exists, else return raw path."""
    p_sample = os.path.join(data_root(), "sample", filename_in_sample)
    if os.path.exists(p_sample):
        return p_sample
    return os.path.join(data_root(), "raw", filename_in_sample)
