from pathlib import Path
from gfatpy.utils.io import read_yaml

RADAR_INFO = read_yaml(Path(__file__).parent.absolute() / 'info.yml')
RADAR_PLOT_INFO = read_yaml(Path(__file__).parent.absolute() / 'plot' / "info.yml")

__all__ = ["RADAR_PLOT_INFO", "RADAR_INFO"]

# from . import preprocessing, retrieval, plot, utils


# __all__ = ["preprocessing", "retrieval", "plot", "utils"]


__doc__ = """
    The top of the radar module that is compatible (at least) with GFAT radar: "NEPHELE" AND "NEBULA"
"""
