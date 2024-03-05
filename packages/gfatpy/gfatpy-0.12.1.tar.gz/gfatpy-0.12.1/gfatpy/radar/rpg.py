from abc import ABC
from pathlib import Path
from pdb import set_trace
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import xarray as xr

from gfatpy.radar import RADAR_PLOT_INFO
from gfatpy.radar.plot.utils import circular_grid
from gfatpy.radar.utils import scanning_to_cartessian


class rpg(ABC):
    def __init__(
        self,
        path: str | Path,
        time_parser: str = "seconds since 2001-01-01 00:00:00 UTC",
    ):
        self.path = path
        self.type = path
        self.level = path
        self.raw = self.initialize_raw(path, time_parser=time_parser)
        self.add_all_products()

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path) -> None:
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File {path} does not exist")
        if path.suffix.lower() != ".nc":
            raise ValueError(f"File {path} is not a netcdf file")
        self._path = path

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, path: Path) -> None:
        self._type = path.name.split(".")[0].split("_")[-1]

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, path: Path) -> None:
        self._level = int(path.name.split(".")[-2][-1])

    @property
    def raw(self) -> xr.Dataset:
        return self._raw

    @raw.setter
    def raw(self, data: xr.Dataset) -> None:
        self._raw = data

    def initialize_raw(
        self, path: Path, time_parser: str = "seconds since 2001-01-01 00:00:00 UTC"
    ) -> xr.Dataset:
        data = xr.open_dataset(path)
        if "Time" in data:
            data = data.rename({"Time": "time"})
        if "range_layers" in data:
            data["range"] = data["range_layers"]
        data.time.attrs["standard_name"] = "time"
        data.time.attrs["long_name"] = "time"
        data.time.attrs["units"] = time_parser
        return data

    def retrieve_PhiDP(self, phiDP: xr.DataArray) -> xr.DataArray:
        phiDP_data = np.rad2deg(
            phiDP
        )  # convert to deg, add -1 because convention is other way around (now the phase shift gets negative, we want it to get positive with range...) TODO: check with Alexander if that makes sense!!
        phiDP_data.attrs = {
            "standard_name": "PhiDP",
            "long_name": "Differential phase shift",
            "units": "deg",
        }
        return phiDP_data

    def retrieve_KDP(
        self, phiDP: xr.DataArray, moving_windows: tuple[int, int] = (30, 5)
    ) -> xr.DataArray:
        # time window: timewindow*timeres gives the amount of seconds over which will be averaged
        # calculate KDP from phidp directly
        range_resolution_array = np.diff(phiDP.range)
        if not "time" in phiDP.dims:
            raise ValueError("No time dimension found")
        if len(phiDP.time) < 2:
            raise ValueError(
                "dimension time found to be less than 2. KDP calculation not possible."
            )

        time_window, range_window = moving_windows
        time_rolled_phiDP = phiDP.rolling(
            time=time_window, min_periods=1, center=True
        ).mean()  # moving window average in time
        range_time_rolled_phiDP = time_rolled_phiDP.rolling(
            range=range_window, min_periods=1, center=True
        ).mean()  # moving window average in range
        specific_diff_phase_shift = range_time_rolled_phiDP.diff(dim="range") / (
            2.0 * abs(range_resolution_array) * 1e-3
        )  # in order to get °/km we need to multiply with 1e-3
        specific_diff_phase_shift = specific_diff_phase_shift.reindex(range=phiDP.range, method="nearest")
        specific_diff_phase_shift = specific_diff_phase_shift.rename(
            "specific_diff_phase_shift"
        )
        specific_diff_phase_shift.attrs = {
            "long_name": "Specific differential phase shift",
            "units": "deg/km",
        }
        return specific_diff_phase_shift

    def retrieve_dBZe(self, Ze: xr.DataArray) -> xr.DataArray:
        dBZe = 10 * np.log10(Ze)
        dBZe.attrs = {"long_name": "Equivalent reflectivity", "units": "dBZe"}
        return dBZe

    def add_all_products_from_LV1(self) -> xr.Dataset:
        # Add products becomes too big.
        # How far can we go with LV1 data? Is it need to use LV0 from the scratch?
        # Implement here the functions made by Chris
        # It may be insteresting to compare the netcdf from the RPGpy and the one from RPG software
        # There are products that can be only calculated from the spectral data
        data = self.raw.copy()
        data["dBZe"] = self.retrieve_dBZe(data["Ze"])
        data["differential_phase"] = self.retrieve_PhiDP(data["differential_phase"])
        data["specific_differential_phase"] = self.retrieve_KDP(data["differential_phase"])
        self.data = data
        return True

    def add_all_products_from_LV0(self) -> xr.Dataset:
        # data['Vspec'] = self.raw['Ze']/(1+self.raw['ldr'])
        # data['Hspec'] = self.raw['Ze'] - data['Vspec']
        # data['sZDR'] = 10*np.log10(self.raw['HSpec']) - 10*np.log10(self.raw['VSpec'])
        # data['new_sZDR'] = self.raw['Ze']*(self.raw['ldr']-1)/(self.raw['ldr']+1)
        # data['sZDRmax'] = data['sZDR'].max(dim='Vel',keep_attrs=True)
        pass

    def add_all_products(self) -> xr.Dataset:
        if self.level == 0:
            self.add_all_products_from_LV0()
        elif self.level == 1:
            self.add_all_products_from_LV1()
        else:
            raise ValueError("Level must be 0 or 1.")

    def plot(self, variable: str | None = None, **kwargs):
        if self.type == "ZEN":
            self.plot_zen(variable, **kwargs)
        elif self.type == "PPI":
            self.plot_ppi(variable, **kwargs)
        elif self.type == "RHI":
            self.plot_rhi(variable, **kwargs)
        else:
            raise ValueError(f"Type {self.type} is not valid")

    def plot_zen(self, variable: str | list[str] | None = None, **kwargs):
        if variable is None:
            variables_to_plot = ["dBZe"]
        if isinstance(variable, str):
            variables_to_plot = [variable]
        elif isinstance(variable, list):
            variables_to_plot = variable
        else:
            raise ValueError(f"Variable {variable} is not valid")
        set_trace()
        for var in variables_to_plot:
            if var not in self.raw:
                raise ValueError(f"Variable {var} is not in the file")
            vmin, vmax = RADAR_PLOT_INFO[var]
            self.raw[f"{var}"].plot(vmin=vmin, vmax=vmax**kwargs)

    def plot_ppi(self, variable: str | None = None, **kwargs) -> tuple[list[Figure], list[Path]]:
        if variable is None:
            variables_to_plot = ["dBZe"]
        elif isinstance(variable, str):
            variables_to_plot = [variable]
        elif isinstance(variable, list):
            variables_to_plot = variable
        else:
            raise ValueError(f"Variable {variable} is not valid")

        # sort data['azimuth'] as increasing and sort the rest of the data accordingly
        data = self.data.sortby("azimuth")
        x, y = scanning_to_cartessian(data["range"], data["azimuth"], data["elevation"])
        mdata = data.mean(dim="time")
        list_of_figs = []
        list_of_paths = []
        for var in variables_to_plot:
            if var not in mdata:
                raise ValueError(f"Variable {var} is not in the file")
            vmin, vmax = RADAR_PLOT_INFO["limits"][var]
            fig, ax = plt.subplots(
                figsize=(10, 10)
            )  # subplot_kw=dict(projection='polar')
            pcm = ax.pcolormesh(
                x/1e3, y/1e3, data[var].values.T, vmin=vmin, vmax=vmax, shading="gouraud"
            )
            
            ax.set_xlim(*RADAR_PLOT_INFO["limits"]["ppi"]["x"])
            ax.set_ylim(*RADAR_PLOT_INFO["limits"]["ppi"]["y"])
            ax.set_xlabel("East-West distance from radar [km]")
            ax.set_ylabel("North-South distance from radar [km]")
            circular_grid(ax, radius = ax.get_xticks())
            ax.set_aspect("equal")
            cbar = plt.colorbar(pcm, ax=ax, shrink=0.7)
            if "units" in data[var].attrs:
                units = data[var].attrs['units']
            else:
                units = "?"
            cbar.set_label(f"{var}, [{units}]")
            fig.tight_layout()
            list_of_figs.append(fig)
            if kwargs.get('savefig', False):
                output_dir = kwargs.get("output_dir", Path.cwd())
                filepath = output_dir / self.path.name.replace(".nc", f"_{var}.png")
                dpi = kwargs.get("dpi", 300)    
                fig.savefig(filepath, dpi=dpi)
                plt.close(fig)
                list_of_paths.append(filepath)
        return list_of_figs, list_of_paths


    def plot_rhi(self, variable: str | None = None, **kwargs):
        pass

    def read_rpg_spectra(self):
        pass

    def read_rpg_spectra_header(self):
        pass

    def __str__(self) -> str:
        return super().__str__()
