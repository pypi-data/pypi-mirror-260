"""EarthNet2021 Toolkit
A library for downloading, evaluating and plotting Earth surface forecasts.
"""

__version__ = "0.3.11"
__author__ = "Vitus Benson, Christian Requena-Mesa"
__credits__ = "Max-Planck-Institute for Biogeochemistry"

from earthnet.coords import get_coords_from_cube, get_coords_from_tile
from earthnet.download import Downloader
from earthnet.download_v2 import download, load_en21x_as_npz, load_minicube
from earthnet.parallel_score import EarthNetScore
from earthnet.plot_cube import cube_gallery, cube_ndvi_timeseries
from earthnet.score_v2 import normalized_NSE, score_over_dataset
