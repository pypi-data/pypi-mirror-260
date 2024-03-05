import re
import shutil
from pathlib import Path
from typing import Iterator

from loguru import logger

from linc.config import Config
from linc import write_nc_legacy

from gfatpy.lidar.utils import LIDAR_INFO

from ..types import LidarName, MeasurementType, Telescope
from .types import Measurement


RAW_FIRST_LETTER = LIDAR_INFO["metadata"]["licel_file_wildcard"]


def to_measurements(glob: Iterator[Path]) -> list[Measurement]:
    """Converts a list of paths to a list of Measurement objects.

    Args:
        glob (Iterator[Path]): Iterator of paths to convert.

    Returns:
        list[Measurement]: List of Measurement objects.
    """    
    measurements = []
    for path in glob:
        new_measurement = Measurement(
            type=MeasurementType(path.name[:2]),
            path=path,
        )
        measurements.append(new_measurement)
    return measurements


def filter_by_type(
    measurements: list[Measurement], mtype: MeasurementType
) -> list[Measurement]:
    """Filter a list of measurements by type.

    Args:
        measurements (list[Measurement]): List of measurements to filter.
        mtype (MeasurementType): Type to filter by.

    Returns:
        list[Measurement]: Filtered list of measurements.
    """    
    return list(
        filter(
            lambda m: m.type == mtype,
            measurements,
        )
    )


def launch_write_nc(
    measurement: Measurement,
    files2convert: list[Path],
    output_dir: Path,
    lidar_name: LidarName,
    telescope: Telescope,
    signal_type: MeasurementType,
    config: Config,
):
    """Launch the write_nc function to convert the raw data to netCDF.

    Args:
        measurement (Measurement): Measurement object to convert (see gfatpy.lidar.nc_convert.utils.Measurement)
        files2convert (list[Path]): List of paths to convert.
        output_dir (Path): Directory to save the netCDF file.
        lidar_name (LidarName): Lidar name (see gfatpy.lidar.nc_convert.types.LidarName).
        telescope (Telescope): Telescope object (see gfatpy.lidar.nc_convert.types.Telescope).
        signal_type (MeasurementType): Signal type (see gfatpy.lidar.nc_convert.types.MeasurementType).
        config (Config): Configuration object (see linc.config.Config).

    Raises:
        Exception: If there is an error writing the netCDF file.
    """    
    # Generate the output path
    result_path = measurement.generate_nc_output_path(
        output_dir,
        lidar_name,
        telescope,
        str(measurement.type),
        signal_type,
    )
    result_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing {result_path.name}")
    try:
        # Write the nc file
        write_nc_legacy(files2convert, result_path, config=config)
    except Exception as e:
        raise Exception(f"Error writing {result_path}: {e}")


# Cleanup function to delete temporary folders
def cleanup_tmp_folders():
    """Delete temporary folders created during the process.

    Raises:
        OSError: If there is an error deleting the temporary folder.
    """    
    pattern = r"tmp_unzipped_[a-zA-Z0-9_]+$"
    for dir_ in Path(__file__).parent.parent.parent.parent.glob("tmp_unzipped_*"):
        if re.search(pattern, dir_.name):
            try:
                shutil.rmtree(dir_)
                print(f"Temporary folder deleted: {dir_}")
            except OSError as e:
                raise OSError(f"Error deleting temporary folder: {e}")
