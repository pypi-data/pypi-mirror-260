from datetime import datetime
from pathlib import Path
from pdb import set_trace
from typing import List, Literal, Tuple

import matplotlib
import numpy as np
import xarray as xr
from loguru import logger
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from gfatpy.lidar.file_manager import filename2info

from gfatpy.lidar.preprocessing.lidar_preprocessing import preprocess
from gfatpy.lidar.utils import LIDAR_INFO, signal_to_rcs
from gfatpy.utils import plot
from gfatpy.utils.io import read_yaml_from_info
from gfatpy.utils.utils import numpy_to_datetime

BoundsType = tuple[float, float] | Literal["auto", "limits"]


def get_norm(
    rcs: np.ndarray,
    scale_bounds: BoundsType,
    color_resolution: int = 128,
) -> matplotlib.colors.BoundaryNorm:
    """Get the color normalization and bounds for the colorbar.

    Args:
        rcs (np.ndarray): Range corrected signal.
        scale_bounds (BoundsType): Bounds for the colorbar.
        color_resolution (int, optional): Colorbar resolution. Defaults to 128.

    Returns:
        matplotlib.colors.BoundaryNorm: Color normalization.
    """    
    match scale_bounds:
        case "auto":
            bounds = np.linspace(0, rcs.max() * 0.6, color_resolution)
        case "limits":
            bounds = np.linspace(rcs.min(), rcs.max(), color_resolution)
        case _:
            bounds = np.linspace(*scale_bounds, color_resolution)

    norm = matplotlib.colors.BoundaryNorm(boundaries=bounds, ncolors=2**8, clip=False)
    logger.debug(f"Color bounds min - max: {bounds.min()} - {bounds.max()}")
    return norm, bounds


def apply_gap_size(ax: matplotlib.axes.Axes, data_array) -> None:  # type: ignore
    """Apply gap size to the x-axis of the plot.

    Args:
        ax (matplotlib.axes.Axes): Axes object.
        data_array (_type_): Data array.
    """    
    diff = data_array.time[1:].values - data_array.time[0:-1].values
    gap_size = 2 * int(
        np.ceil(
            np.median(np.median(diff).astype("timedelta64[s]").astype("float") / 60)
        )
    )
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))  # Formato de hora: minutos
    
    plot.gapsizer(
        ax,
        data_array.time.values.astype("M8[ms]").astype("O"),
        data_array.range.values,
        gap_size,
        "#c7c7c7",
    )


def quicklook_xarray(
    data_array: xr.DataArray,
    lidar_name: str,
    location: str = 'Granada',
    is_rcs: bool = True,
    scale_bounds: BoundsType = "auto",
    colormap: str | matplotlib.colors.Colormap = "jet",
    ylims: Tuple[float, float] = (0.0, 14000.0),
) -> Tuple[Figure, Axes]:
    """Plot a quicklook of a xarray.DataArray

    Args:
        data_array (xr.DataArray): Lidar signal or rcs from `lidar.preprocess`
        is_rcs (bool, optional): To indicate if the data is RCS or not. Defaults to True.
        scale_bounds (BoundsType, optional): scale bounds for the colorbar. Defaults to "auto".
        colormap (str | matplotlib.colors.Colormap, optional): colormap of the colorbar. Defaults to "jet".

    Returns:
        tuple[Figure, Axes]: Figure and Axes objects
    """

    #Convert cmap str to matplotlib colormap
    if isinstance(colormap, str):
        colormap = plt.get_cmap(colormap)
    cmap = colormap.copy()
    cmap.set_extremes(over="white")

    #Define channel
    channel = data_array.name.split('_')[1]
    
    try:
        if is_rcs:
            rcs = data_array.values
        else:
            rcs = signal_to_rcs(data_array.values, data_array.range.values)

        fig, ax = plt.subplots(figsize=(15, 5))
        norm, bounds = get_norm(rcs, scale_bounds)       

        q = ax.pcolormesh(
            data_array.time,
            data_array.range/1000.,
            rcs.T,
            cmap=cmap,
            norm=norm,
        )

        ax.set_xlabel(r"Time, $[UTC]$")
        ax.set_ylabel(r"Height, $[km, \, agl]$")
        ax.set_ylim(ylims[0]/1000., ylims[1]/1000.)

        plot.watermark(ax, zoom=0.6, alpha=0.6)
        
        datestr = datetime.strftime(numpy_to_datetime(data_array.time[1].values), "%Y-%m-%d")
        ax.set_title(f"{location} | {lidar_name.upper()}-{channel} | {datestr}")      
        
        apply_gap_size(ax, data_array=data_array)

        # Agregar la magnitud y unidades a la barra de color
        magnitud = f"RCS@{channel[:-3]}nm"
        unidades = "a.u."     
        ticks = np.linspace(bounds.min(), bounds.max(), 9)
        colorbar = fig.colorbar(q, ticks=ticks, extend='max')

        # Crear el texto de magnitud y unidades
        text = f"{magnitud} [{unidades}]"

        # Calcular la mitad de la altura de la barra de color
        mid_height = (colorbar.ax.get_ylim()[0] + colorbar.ax.get_ylim()[1]) / 2

        # Añadir el texto a la barra de color girado 90 grados y 3 cm a la derecha de los valores
        x_position = 1.2  # Cambiar la coordenada x según sea necesario
        y_position = mid_height
        x_offset = 4  # 3 cm a la derecha (puede ajustarse)
        colorbar.ax.text(
            x_position + x_offset,
            y_position,
            text,
            rotation=90,
            va="center",
            ha="left",
            fontsize=12,
        )

        q.cmap.set_over("white")  # type: ignore
    except Exception as e:
        raise e
    return fig, ax


def quicklook_dataset(
    dataset: xr.Dataset,
    channel: str,
    /,    
    scale_bounds: BoundsType = "auto",
    colormap: str | matplotlib.colors.Colormap = "jet",
    ylims: Tuple[float, float] = (0.0, 14000.0),
) -> Tuple[Figure, Axes]:
    """Plot a quicklook of a xarray.DataArray

    Args:
        data_array (xr.DataArray): Lidar signal or rcs from `lidar.preprocess`
        is_rcs (bool, optional): To indicate if the data is RCS or not. Defaults to True.
        scale_bounds (BoundsType, optional): scale bounds for the colorbar. Defaults to "auto".
        colormap (str | matplotlib.colors.Colormap, optional): colormap of the colorbar. Defaults to "jet".

    Returns:
        tuple[Figure, Axes]: Figure and Axes objects
    """

    #Convert cmap str to matplotlib colormap
    if isinstance(colormap, str):
        colormap = plt.get_cmap(colormap)
    cmap = colormap.copy()
    cmap.set_extremes(over="white")
    
    data_array = dataset[f"signal_{channel}"]

    #Get lidar name from dataset
    lidar_name = dataset.attrs['location'].lower()

    quicklook_xarray(data_array, lidar_name = lidar_name, location = 'Granada', is_rcs=False, scale_bounds=scale_bounds, colormap=colormap, ylims=ylims)

    try:        
        rcs = signal_to_rcs(data_array.values, data_array.range.values)

        fig, ax = plt.subplots(figsize=(15, 5))
        norm, bounds = get_norm(rcs, scale_bounds)       

        q = ax.pcolormesh(
            data_array.time,
            data_array.range/1000.,
            rcs.T,
            cmap=cmap,
            norm=norm,
        )

        ax.set_xlabel(r"Time, $[UTC]$")
        ax.set_ylabel(r"Height, $[km, \, agl]$")
        ax.set_ylim(ylims[0]/1000., ylims[1]/1000.)

        datestr = datetime.strftime(numpy_to_datetime(data_array.time[1].values), "%Y%m%d")        
        plot.title1(f"{data_array.name} | {datestr}", 2)


        plot.watermark(ax, zoom=0.6, alpha=0.6)
        apply_gap_size(ax, data_array=data_array)

        # Agregar la magnitud y unidades a la barra de color
        magnitud = "RCS"
        unidades = "a.u."     
        ticks = np.linspace(bounds.min(), bounds.max(), 9)
        colorbar = fig.colorbar(q, ticks=ticks, extend='max')

        # Crear el texto de magnitud y unidades
        text = f"{magnitud} [{unidades}]"

        # Calcular la mitad de la altura de la barra de color
        mid_height = (colorbar.ax.get_ylim()[0] + colorbar.ax.get_ylim()[1]) / 2

        # Añadir el texto a la barra de color girado 90 grados y 3 cm a la derecha de los valores
        x_position = 1.2  # Cambiar la coordenada x según sea necesario
        y_position = mid_height
        x_offset = 4  # 3 cm a la derecha (puede ajustarse)
        colorbar.ax.text(
            x_position + x_offset,
            y_position,
            text,
            rotation=90,
            va="center",
            ha="left",
            fontsize=12,
        )

        q.cmap.set_over("white")  # type: ignore
    except Exception as e:
        raise e
    return fig, ax

def quicklook_from_file(
    filepath: Path | str, channels: List[str], output_dir: Path | str | None = None, scale_bounds: BoundsType = "auto", apply_ov: bool = True    
):
    # Define output directory
    if output_dir is None:
        output_dir = Path.cwd()
    elif isinstance(output_dir, str):
        output_dir = Path(output_dir)
    else:
        if not output_dir.exists():
            raise ValueError(f"Output directory {output_dir} does not exist.")

    # Check filepath
    if isinstance(filepath, str):
        filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} does not exist.")
    
    # Get lidar name from filepath    
    nickname, _, _, _, _, target_date = filename2info(filepath.name)    
    lidar_name = LIDAR_INFO["metadata"]["nick2name"][nickname]
    
    # Get INFO
    INFO = read_yaml_from_info(nickname, target_date)

    if apply_ov:
        channels2load = channels.copy()
        for channel_ in channels2load:
            if 'f' in channel_:
                overlap_channel_ = INFO['overlap_channels'][channel_]
                if overlap_channel_ not in channels2load:
                    channels2load.append(overlap_channel_)
    
    lidar = preprocess(filepath, channels=channels2load, apply_bg=True, apply_dc=True, apply_dt=False, apply_bz=True, apply_ov=apply_ov)    

    # Get location from dataset 
    location = lidar.attrs['location']

    # Get date string
    datestr = datetime.strftime(numpy_to_datetime(lidar.time[1].values), "%Y%m%d")

    for channel_ in channels:
        fig, _ = quicklook_xarray(lidar[f"signal_{channel_}"], lidar_name=lidar_name, location=location, is_rcs=False, scale_bounds=scale_bounds)
        fig.savefig(
            output_dir / f"quicklook_{nickname}_{channel_}_{datestr}.png",
            dpi=600,
            bbox_inches="tight",
        )
        plt.close(fig)
    lidar.close()

# TODO: this should be the default implemetation rather than filelist argument
