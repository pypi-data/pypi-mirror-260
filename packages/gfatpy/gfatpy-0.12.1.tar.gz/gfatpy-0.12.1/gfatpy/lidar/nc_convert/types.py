from pathlib import Path
from datetime import datetime as dt, timedelta
from pdb import set_trace
import re
import zipfile

from gfatpy.lidar.file_manager import info2general_path, info2path
from gfatpy.lidar.utils import filter_wildcard
from gfatpy.lidar.utils import get_532_from_telescope, licel_to_datetime, to_licel_date_str

from gfatpy.utils.io import unzip_file
from gfatpy.lidar.utils import LIDAR_INFO

from ..types import LidarName, MeasurementType, Telescope

RAW_FIRST_LETTER = LIDAR_INFO["metadata"]["licel_file_wildcard"]


class Measurement:
    path: Path
    type: MeasurementType
    datetime: dt
    is_zip: bool = False
    unzipped_path: Path | None = None
    files: list[str] = []
    has_dc: bool = False
    dc_path: Path | None = None
    linked_measurements: list = []

    def __init__(self, path: Path, type: MeasurementType, **kwargs):
        self.path = path
        self.type = type
        self.is_zip = self.path.suffix.endswith("zip")
        self.datetime = self.extract_datetime()
        self.filenames = [file.name for file in self.get_filepaths()]
        self.sub_dirs = self.extract_folders()
        self.has_dc = self.check_for_dc()
        self.dc_path = self.get_dc()
        self.unzipped_path = None

    def extract_datetime(self) -> dt:
        """get datetime from the measurement path

        Returns:
            dt: datetime object
        """        
        formatted_date = self.path.name.split(".")[0][3:]
        return dt.strptime(formatted_date, r"%Y%m%d_%H%M")

    # def extract_filenames(self, wildcard: str = r"\.\d+$") -> list:
    #     """Extract filenames from the measurement path

    #     Args:
    #         wildcard (str, optional): wildcard pattern to filter the files. Defaults to r"\.\d+$".

    #     Raises:
    #         Exception: No files found in the directory to meet the wildcard.

    #     Returns:
    #         list: list of filenames.
    #     """        
    #     # Extract files from ZIP or directory based on wildcard pattern
    #     files = []
    #     if self.is_zip:

    #         unzip_file( self.path, pattern_or_list=wildcard, destination=destination )

    #         with zipfile.ZipFile(self.path, "r") as zip_ref:
    #             file_list = zip_ref.namelist()
    #             files = [
    #                 Path(file).name
    #                 for file in file_list
    #                 if (not Path(file).is_dir() and re.search(wildcard, Path(file).name))
    #             ]
    #     elif self.path.is_dir():            
    #         files = [file.name for file in self.path.rglob(wildcard)]
    #         if len(files) == 0:
    #             raise Exception(f"No files found in {self.path} to meet the wildcard {wildcard}")
    #     return files

    def extract_folders(self) -> list[str]:
        """Extract sub-directories from the measurement path

        Returns:
            list[str]: list of sub-directories.
        """        
        folders = []
        path = self.path  # Store path in a local variable for use in the method
        if self.is_zip:
            with zipfile.ZipFile(path, "r") as zip_ref:
                file_list = zip_ref.namelist()
                folders = [
                    file.split("/")[-2] for file in file_list if file.endswith("/")
                ]
        elif path.is_dir():
            folders = [f.name for f in path.iterdir() if f.is_dir()]
        return folders

    def get_dc(self) -> Path | None:
        """Get the path for the DC type measurement

        Returns:
            Path | None: Path for the DC type measurement. None if it does not exist.
        """        
        # Get the path for the DC type measurement
        if self.type == MeasurementType.DC:
            return None
        dc_path = self.path.parent / self.path.name.replace(
            self.type, MeasurementType.DC
        )
        return dc_path if dc_path.exists() else None

    def check_for_dc(self) -> bool:
        """Check if the DC type measurement exists 

        Returns:
            bool: True if the DC type measurement exists. False otherwise.
        """        
        if self.type == MeasurementType.DC:
            return False

        dc_path = self.path.parent / self.path.name.replace(
            self.type, MeasurementType.DC
        )
        return dc_path.exists()

    def extract_zip(
        self, pattern_or_list: str = r'\.\d+$', destination: Path | None = None
    ) -> None:
        """Extract the zip file

        Args:
            pattern_or_list (str, optional): pattern or list of patterns. Defaults to r'\.\d+$'.
            destination (Path | None, optional): Directory to extract files. Defaults to None (extract to the same directory as the zip file).
        """        
        self.unzipped_path = unzip_file( self.path, pattern_or_list=pattern_or_list, destination=destination )


    def has_target_date(self, date: dt) -> bool:
        """Check if the measurement has the target date

        Args:
            date (dt): Target date

        Returns:
            bool: True if the measurement has the target date. False otherwise.
        """        
        has_target_date = False
        for file in self.files:
            match = re.search(f"{RAW_FIRST_LETTER}{to_licel_date_str(date)}*", file)
            if match != None and match.span()[1] > 6: 
                has_target_date = True
                break
        return has_target_date

    def generate_nc_output_path(
        self,
        output_path: Path,
        lidar_name: str,
        telescope: Telescope,
        measurement_type: str,
        signal_type: MeasurementType,
    ) -> Path:
        """Generate the output path for the netCDF file

        Args:
            output_path (Path): Directory to save the netCDF file.
            lidar_name (str): Lidar name.
            telescope (Telescope): Telescope object (see gfatpy.lidar.nc_convert.types.Telescope).
            measurement_type (str): Measurement type (eg., RS, DC, etc.).
            signal_type (MeasurementType): Signal type (see gfatpy.lidar.nc_convert.types.MeasurementType). 

        Returns:
            Path: Output path for the netCDF file.
        """        
        return info2path(
            lidar_name=lidar_name,
            channel=get_532_from_telescope(telescope),
            measurement_type=measurement_type,
            signal_type=signal_type,
            date=self.datetime,
            dir=output_path,
        )

    def find_prev_paths(
        self, number_of_previous_days: int, lidar_name: LidarName, raw_dir: Path
    ) -> list[Path]:
        """Find the paths for the previous days

        Args:
            number_of_previous_days (int): Number of previous days to look for.
            lidar_name (LidarName): Lidar name (see gfatpy.lidar.nc_convert.types.LidarName).
            raw_dir (Path): Directory for the raw data.

        Returns:
            list[Path]: List of paths for the previous days.
        """        
        current_date = self.datetime
        prev_paths = [
            info2general_path(
                lidar_name.value,
                date=current_date - timedelta(days=n_day),
                data_dir=raw_dir,
            )
            for n_day in range(1, number_of_previous_days + 1)
        ]
        # Remove paths that do not exist
        previous_paths = [prev_path for prev_path in prev_paths if prev_path.exists()]
        return previous_paths

    def add_linked_measurements(self, measurements: list) -> None:
        """Add linked measurements to the measurement object.

        Args:
            measurements (list): List of measurements.
        """        
        # Add linked measurements to the measurement object
        # Linked measurements are measurements with the same date and type

        combine_list = self.linked_measurements + measurements
        self.linked_measurements = list(set(combine_list))
        
    
    def get_filepaths(self, pattern_or_list: str = r"\.\d+$", within_period: tuple[dt, dt] | None = None ) -> set[Path]:
        """Get the files from a measurement

        Args:
            measurement (Measurement): Measurement object

        Returns:
            set[Path]: Set of licel files
        """

        # Get files from the measurement main path
        if self.is_zip:
            if self.unzipped_path is None:
                self.extract_zip(pattern_or_list=pattern_or_list)
            dir_ = self.unzipped_path
        else:
            dir_ = self.path

        found_files = set(filter_wildcard(dir_))

        # Get files from linked measurements
        for linked_measurement in self.linked_measurements:
            if linked_measurement.is_zip:
                if linked_measurement.unzipped_path is None:
                    linked_measurement.extract_zip(pattern_or_list=pattern_or_list)
                dir_ = linked_measurement.unzipped_path
            else:
                dir_ = linked_measurement.path
            found_files.update(filter_wildcard(dir_))

        # Filter files2convert by larger than date_ini and smaller than date_end
        if within_period is not None:
            date_ini, date_end = within_period
            selected_files = { licel_ for licel_ in found_files if date_ini <= licel_to_datetime(licel_.name) <= date_end }
        else:
            selected_files = found_files
        return selected_files

    def __str__(self):
        return f"Measurement Object\nPath: {self.path}\nType: {self.type}\nDatetime: {self.datetime}\nIs ZIP: {self.is_zip}\nFiles: {self.files}\nSub-directories: {self.sub_dirs}\nDC Path: {self.dc_path}\nHas DC: {self.has_dc}\nUnzipped Path: {self.unzipped_path}\n\nLinked Measurements: {self.linked_measurements}\n"
