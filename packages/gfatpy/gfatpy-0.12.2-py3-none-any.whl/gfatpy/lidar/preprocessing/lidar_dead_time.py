from pathlib import Path
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pdb import set_trace
from gfatpy.lidar.preprocessing import preprocess
from gfatpy.utils.plot import color_list


def binning(
    an: np.ndarray,
    pc: np.ndarray,
    pc_binning_range: tuple[float, float],
    pc_bin_width: float,
    channel_pc: str,
    datetime: str,
    plot_dir: Path,
    savefig: bool,
):
    def plot_binning(
        an: np.ndarray,
        pc: np.ndarray,
        median_pc: np.ndarray,
        mean_an: np.ndarray,
        std_an: np.ndarray,
        channel_pc: str,
        datetime: str,
        plot_dir: Path,
        savefig: bool,
    ):
        fig, ax = plt.subplots(figsize=[15, 5])
        ax.scatter(pc, an, c="grey", s=0.5, label="raw")
        ax.errorbar(
            median_pc,
            mean_an,
            yerr=std_an,
            linestyle="None",
            marker=".",
            color="red",
            label="binning",
        )
        ax.set_xlabel("PC signal, [MHz]")
        ax.set_ylabel("dc-corrected AN signal, [mV]")
        ax.set_title(f"{channel_pc} | {datetime}")
        ax.set_yscale("linear")
        ax.set_xlim(*pc_binning_range)
        ax.legend(fontsize=10, loc="upper right")
        if savefig:
            plt.savefig(plot_dir / f"binning_{channel_pc}_{datetime}.png")
        plt.close(fig)

    # Apply binning to pc and an
    bins = np.arange(
        pc_binning_range[0], pc_binning_range[1] + pc_bin_width, pc_bin_width
    )

    # Use numpy.digitize to get the bin indices for each element in signal_pc
    bin_indices = np.digitize(pc, bins)

    # Compute the median, mean, and standard deviation for each bin
    median_pc = np.array([np.median(pc[bin_indices == i]) for i in range(1, len(bins))])
    mean_an = np.array([np.mean(an[bin_indices == i]) for i in range(1, len(bins))])
    std_an = np.array([np.std(an[bin_indices == i]) for i in range(1, len(bins))])
    isnan = np.logical_and(np.isnan(median_pc), np.isnan(mean_an), np.isnan(std_an))

    # Plot binning
    plot_binning(
        an,
        pc,
        median_pc,
        mean_an,
        std_an,
        channel_pc,
        datetime,
        plot_dir,
        savefig=savefig,
    )

    return median_pc[~isnan], mean_an[~isnan], std_an[~isnan]


def get_valid_an_pc_values(
    signal_an: xr.DataArray,
    signal_pc: xr.DataArray,
    pc_threshold: float,
    an_threshold: float,
) -> tuple[np.ndarray, np.ndarray]:
    gl_condition = np.logical_and(
        signal_an.values > an_threshold, signal_pc.values < pc_threshold
    )
    an = np.concatenate(signal_an.where(gl_condition).values, axis=0)
    pc = np.concatenate(signal_pc.where(gl_condition).values, axis=0)
    isnan = np.logical_and(np.isnan(an), np.isnan(pc))
    an = an[~isnan]
    pc = pc[~isnan]
    return an, pc


def cost_function(
    tau_range: np.ndarray,
    mean_an: np.ndarray,
    median_pc: np.ndarray,
    std_an: np.ndarray,
    channel_pc: str,
    datetime: str,
    savefig: bool,
    plot_dir: Path,
) -> tuple[np.ndarray, float]:
    
    def plot_cost_function(
        tau_range: np.ndarray,
        J: np.ndarray,
        channel_pc: str,
        plot_dir: Path,
        datetime: str,
        optimal_tau_index: int,
        savefig: bool,
    ):
        logJ = np.log(J)
        optimal_tau = tau_range[optimal_tau_index]
        fig, ax = plt.subplots(figsize=[15, 5])
        ax.plot(tau_range, logJ, c="blue", lw=2, label="J", zorder=1)
        ax.scatter(
            optimal_tau,
            logJ[optimal_tau_index],
            marker="p",
            s=50,
            color="yellow",
            label=f"optimal tau = {optimal_tau:.2f} ns",
            zorder=2,
        )
        ax.set_ylabel("log(J), [#]")
        ax.set_xlabel(r"$\tau$, [ns]")
        ax.minorticks_on()
        ax.grid(True, which="both", linestyle=":", linewidth=0.5, color=[0.3, 0.3, 0.3])
        ax.set_title(f"{channel_pc} | {datetime}")
        ax.legend(fontsize=10, loc="upper center")
        if savefig:
            plt.savefig(plot_dir / f"cost_function_{channel_pc}_{datetime}.png")
        plt.close(fig)

    J = np.nan * np.ones(len(tau_range))
    for idx, tau_ in enumerate(tau_range):
        dt_pc = median_pc / (1 - tau_ * median_pc * 1e-3)
        if not np.isnan(dt_pc).any() and not np.isnan(mean_an).any():
            try:
                fit_values = np.polyfit(dt_pc, mean_an, 1)
                virtual_an = np.polyval(fit_values, dt_pc)
            except Exception as e:                
                print(e)
                raise ValueError("Error in fitting binned an and pc")

            try:
                # Cost function
                idx_zero = std_an == 0
                J[idx] = np.sum(
                    (mean_an[~idx_zero] - virtual_an[~idx_zero]) ** 2
                    / std_an[~idx_zero] ** 2
                ) / len(mean_an)
            except Exception as e:                
                print(e)
                raise ValueError("Error in cost function")
    optimal_tau_index = np.log(J).argmin()

    plot_cost_function(
        tau_range=tau_range,
        J=J,
        channel_pc=channel_pc,
        plot_dir=plot_dir,
        datetime=datetime,
        optimal_tau_index=optimal_tau_index,
        savefig=savefig,
    )
    return J, tau_range[optimal_tau_index]


def plot_influence_of_dead_time_correction(
    tau_range: np.ndarray,
    mean_an: np.ndarray,
    median_pc: np.ndarray,
    channel_pc: str,
    datetime: str,
    plot_dir: Path,
    savefig: bool,
):
    fig, ax = plt.subplots(figsize=[15, 5])
    h0 = ax.scatter(mean_an, median_pc, label="original")
    colors = color_list(len(tau_range))
    handles = [None] * len(tau_range)
    for idx, tau_ in enumerate(tau_range):
        dt_pc = median_pc / (1 - tau_ * median_pc * 1e-3)
        handles[idx] = ax.scatter(
            mean_an, dt_pc, color=colors[idx], label=f"tau={tau_:.2f} ns"
        )
    ax.legend(
        [h0, handles[0], handles[-1]],
        ["original", f"tau={tau_range[0]:.2f} ns", f"tau={tau_range[-1]:.2f} ns"],
        fontsize=10,
        loc="upper left",
    )
    # ax.legend([h0, handles[0], handles[-1]], fontsize=10, loc="upper left")
    ax.set_ylabel("dt-corrected PC signal, [MHz]")
    ax.set_xlabel("dc-corrected AN signal, [mV]")
    ax.set_title(datetime)
    ax.grid(True, which="both", linestyle=":", linewidth=0.5, color=[0.3, 0.3, 0.3])
    if savefig:
        plt.savefig(plot_dir / f"pc_taus_{channel_pc}_{datetime}.png")
    plt.close(fig)


def plot_gluing_thresholds(
    signal_an: xr.DataArray,
    signal_pc: xr.DataArray,
    pc_threshold: float,
    an_threshold: float,
    datetime: str,
    plot_dir: Path,
    savefig: bool,
    range_limits: tuple[float, float],
):
    channel_pc = signal_pc.name.split("_")[-1]

    fig, ax = plt.subplots(figsize=[15, 5])
    lan = signal_an.plot.line(x="range", c="grey", lw=0.5, label="an")
    lpc = signal_pc.plot.line(x="range", c="black", lw=0.5, label="pc")

    l1 = plt.hlines(
        pc_threshold, xmin=0, xmax=10000, color="darkred", ls="--", label="Cmax"
    )
    l2 = plt.hlines(
        an_threshold,
        xmin=0,
        xmax=10000,
        color="violet",
        ls="--",
        label="bg_threshold_an",
    )

    ax.set_title(f"{channel_pc} | {datetime}")
    ax.set_yscale("log")
    ax.set_ylim(0.01, 3000)
    ax.set_xlim(*range_limits)
    ax.legend(handles=[lan[0], lpc[0], l1, l2], fontsize=10, loc="upper right")

    if savefig:
        plt.savefig(plot_dir / f"gluing_thresholds_{channel_pc}_{datetime}.png")
    plt.close(fig)


def dead_time_finder_by_channel(
    lidar: Path,
    channel_an: str,
    channel_pc: str,
    pc_threshold: float,
    an_threshold: float,
    tau_range: list,
    pc_binning_range: tuple[float, float],
    pc_bin_width: float,
    plot_dir: Path,
    savefig: bool,
    range_limits: tuple[float, float],
) -> float:
    datetime = lidar.time.values[0].astype(str).split("T")[0].replace("-", "")
    signal_an = lidar[f"signal_{channel_an}"]
    signal_pc = lidar[f"signal_{channel_pc}"]

    plot_gluing_thresholds(
        signal_an=signal_an,
        signal_pc=signal_pc,
        pc_threshold=pc_threshold,
        an_threshold=an_threshold,
        datetime=datetime,
        plot_dir=plot_dir,
        savefig=savefig,
        range_limits=range_limits,
    )

    # get valid an and pc values
    an, pc = get_valid_an_pc_values(
        signal_an=signal_an,
        signal_pc=signal_pc,
        pc_threshold=pc_threshold,
        an_threshold=an_threshold,
    )

    if len(an) < 100 or len(pc) < 100:
        print(f"Empty arrays for {channel_pc} | {datetime}")
        return np.nan

    # apply binning
    median_pc, mean_an, std_an = binning(
        an=an,
        pc=pc,
        pc_binning_range=pc_binning_range,
        pc_bin_width=pc_bin_width,
        channel_pc=channel_pc,
        datetime=datetime,
        plot_dir=plot_dir,
        savefig=savefig,
    )
    
    # Plot influence of dead time correction
    plot_influence_of_dead_time_correction(
        tau_range=tau_range,
        mean_an=mean_an,
        median_pc=median_pc,
        channel_pc=channel_pc,
        datetime=datetime,
        plot_dir=plot_dir,
        savefig=savefig,
    )

    # Retrieve cost function
    J, optimal_tau = cost_function(
        tau_range=tau_range,
        mean_an=mean_an,
        median_pc=median_pc,
        std_an=std_an,
        channel_pc=channel_pc,
        datetime=datetime,
        savefig=savefig,
        plot_dir=plot_dir,
    )    

    #Check if optimal tau is out of range
    if optimal_tau == tau_range[0] or optimal_tau == tau_range[-1]:
        print(f'Warning! {datetime} | {channel_pc} : tau out of range')
        return np.nan
    print(f"{datetime} | Optimal tau for {channel_pc} = {optimal_tau} ns")
    
    return optimal_tau


def estimate_daily_dead_time(
    file: Path | str,
    tau_dir: Path | str | None = None,
    tau_range: list | np.ndarray = np.arange(2, 10, 0.1),
    crop_range: tuple = (0, 15000),
    pc_threshold: float = 50,
    an_threshold: float = 0.1,
    pc_binning_range: tuple = (0, 60),
    pc_bin_width=1,
    range_limits: tuple[float, float] = (0, 10000),
    savefig: bool = False,
) -> Path:
    # Management file type
    if isinstance(file, str):
        file = Path(file)
    if file.exists() == False:
        raise FileNotFoundError(f"{file} does not exist")
    if file.suffix != ".nc":
        raise TypeError(f"{file} is not a netcdf file")

    # Management tau_dir type
    if isinstance(tau_dir, str):
        tau_dir = Path(tau_dir)
    if tau_dir is None:
        tau_dir = Path.cwd()

    # Management tau_range type
    if isinstance(tau_range, list):
        tau_range = np.array(tau_range)
    if tau_range.ndim != 1:
        raise ValueError(f"tau_range must be a 1D array")

    # Read
    lidar = preprocess(
        file,
        apply_dt=False,
        save_bg=False,
        save_dc=True,
        apply_bz=False,
        crop_ranges=crop_range,
    )
    datetime = lidar.time.values[1].astype(str).split("T")[0].replace("-", "")
    
    if savefig:
        plot_dir = tau_dir / f"plots_{datetime}"
        if plot_dir.exists() == False:
            try:
                plot_dir.mkdir()
            except Exception as e:
                print(e)
                raise ValueError(f"Error creating {plot_dir}")

    # Create tau dictionary
    optimal_taus = {}

    for channel_ in [
        channel_ for channel_ in lidar.channel.values if channel_.endswith("a")
    ]:
        channel_an, channel_pc = channel_, channel_.replace("a", "p")
        if channel_pc in lidar.channel:

            optimal_taus[channel_pc] = dead_time_finder_by_channel(
                lidar=lidar,
                channel_an=channel_an,
                channel_pc=channel_pc,
                pc_threshold=pc_threshold,
                an_threshold=an_threshold,
                pc_binning_range=pc_binning_range,
                pc_bin_width=pc_bin_width,
                plot_dir=plot_dir,
                savefig=savefig,
                tau_range=tau_range,
                range_limits=range_limits,
            )

    # Save optimal_taus
    tau_da = xr.DataArray(
        list(optimal_taus.values()),
        coords=[list(optimal_taus.keys())],
        dims=["channel"],
    )
    tau_da.attrs["date"] = datetime
    output_file = tau_dir / f"alh_dead-time_{datetime}.nc"
    tau_da.to_netcdf(output_file)
    return output_file
