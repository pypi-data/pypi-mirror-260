from pdb import set_trace
from typing import Any, Tuple
from matplotlib import pyplot as plt
import numpy as np
from scipy import integrate
from scipy.integrate import cumulative_trapezoid as cumtrapz

from loguru import logger

from gfatpy.lidar.utils import refill_overlap


def klett_rcs(
    rcs_profile: np.ndarray,
    range_profile: np.ndarray,
    beta_mol_profile: np.ndarray,
    lr_part: float | np.ndarray = 45.,
    lr_mol: float = 8 * np.pi / 3,
    reference: Tuple[float, float] = (8000, 8500),
    beta_aer_ref: float = 0,
) -> np.ndarray:
    """Calculate aerosol backscattering using Classical Klett algorithm verified with Fernald, F. G.: Appl. Opt., 23, 652-653, 1984.

    Args:
        rcs_profile (np.ndarray): 1D signal profile.
        range_profile (np.ndarray): 1D range profile with the same shape as rcs_profile.
        beta_mol_profile (np.ndarray): 1D array containing molecular backscatter values.
        lr_mol (float): Molecular lidar ratio (default value based on Rayleigh scattering).
        lr_part (float, optional): Aerosol lidar ratio (default is 45 sr).
        reference (Tuple[float, float], optional): Range interval (ymin and ymax) for reference calculation. Defaults to (8000, 8500).
        beta_aer_ref (float, optional): Aerosol backscatter at reference range (ymin and ymax). Defaults to 0.

    Returns:
        np.ndarray: Aerosol-particle backscattering profile.
    """

    if isinstance(lr_part, float):
        lr_part = np.full(len(range_profile), lr_part)
    if isinstance(lr_mol, float):
        lr_mol = np.full(len(range_profile), lr_mol)
    
    ymin, ymax = reference

    particle_beta = np.zeros(len(range_profile))

    ytop = np.abs(range_profile - ymax).argmin()

    range_resolution = np.median(np.diff(range_profile))

    idx_ref = np.logical_and(range_profile >= ymin, range_profile <= ymax)

    if not idx_ref.any():
        raise ValueError("Range [ymin, ymax] out of rcs size.")

    calib = np.nanmean(
        rcs_profile[idx_ref] / (beta_mol_profile[idx_ref] + beta_aer_ref)
    )
    
    #from Correct(ed) Klett–Fernald algorithm for elastic aerosol backscatter retrievals: a sensitivity analysis 
    # Johannes Speidel* AND Hannes Vogelmann
    # https://doi.org/10.1364/AO.465944
    # Eq. 10
    # Reminder: BR = lr_mol, BP = lr_part
    
    integral_in_Y = np.flip(cumtrapz( np.flip((lr_mol[:ytop] - lr_part[:ytop]) * beta_mol_profile[:ytop]), dx=range_resolution, initial=0) )
    exp_Y = np.exp( -2 * integral_in_Y)
    
    integral_in_particle_beta = np.flip(cumtrapz(np.flip(lr_part[:ytop] * rcs_profile[:ytop] * exp_Y), dx=range_resolution, initial=0))

    total_beta = (rcs_profile[:ytop] * exp_Y) / (calib + 2 * integral_in_particle_beta)
    
    particle_beta[:ytop] = total_beta - beta_mol_profile[:ytop]
    
    return particle_beta


def klett_likely_bins(
    rcs_profile: np.ndarray[Any, np.dtype[np.float64]],
    att_mol_beta: np.ndarray[Any, np.dtype[np.float64]],
    heights: np.ndarray[Any, np.dtype[np.float64]],
    min_height: float = 1000,
    max_height: float = 1010,
    window_size: int = 50,
    step: int = 1,
):
    window_size // 2
    i_bin, e_bin = np.searchsorted(heights, [min_height, max_height])

    for i in np.arange(i_bin, e_bin + 1):
        rcs_profile / rcs_profile

    # return rcs_profile


def find_lidar_ratio(
    rcs: np.ndarray[Any, np.dtype[np.float64]],
    height: np.ndarray[Any, np.dtype[np.float64]],
    beta_mol: np.ndarray[Any, np.dtype[np.float64]],
    lr_mol: float,
    reference_aod: float,
    mininum_height: float = 0,
    lr_initial: float = 50,
    lr_resol: float = 1,
    max_iterations: int = 100,
    rel_diff_aod_percentage_threshold: float = 1,
    debugging: bool = False,
    klett_reference: Tuple[float, float] = (7000, 8000),
) -> Tuple[float, float | None, bool]:
    """Iterative process to find the lidar ratio (lr) that minimizes the difference between the measured and the calculated aerosol optical depth (aod).

    Args:
        rcs (np.ndarray[Any, np.dtype[np.float64]]): Range Corrected Signal
        height (np.ndarray[Any, np.dtype[np.float64]]): Range profile
        beta_mol (np.ndarray[Any, np.dtype[np.float64]]): Molecular backscattering coefficient profile
        lr_mol (float): Molecular lidar ratio
        reference_aod (float): Reference aerosol optical depth
        mininum_height (float, optional): Fullover height. Defaults to 0.
        lr_initial (float, optional): _description_. Defaults to 50.
        lr_resol (float, optional): _description_. Defaults to 1.
        max_iterations (int, optional): _description_. Defaults to 100.
        rel_diff_aod_percentage_threshold (float, optional): _description_. Defaults to 1.
        debugging (bool, optional): _description_. Defaults to False.
        klett_reference (Tuple[float, float], optional): _description_. Defaults to (7000, 8000).

    Returns:
        Tuple[float, float | None, bool]: _description_
    """

    # Calculate range resolution
    range_resolution = np.median(np.diff(height)).item()

    # Initialize loop
    lr_, iter_, run, success = lr_initial, 0, True, False
    rel_diff_aod = None

    while run:
        iter_ = iter_ + 1

        # Calculate aerosol backscatter
        beta_ = klett_rcs(
            rcs, height, beta_mol, lr_part=lr_, lr_mol=lr_mol, reference=klett_reference
        )

        # Refill beta profile from minimum height to surface to avoid overlap influence
        beta_ = refill_overlap(beta_, height)

        # Calculate aerosol optical depth
        aod_ = integrate.simps(beta_ * lr_, dx=range_resolution)

        # Calculate relative difference between measured and calculated aod
        rel_diff_aod = 100 * (aod_ - reference_aod) / reference_aod

        if debugging:
            print(
                "lidar_aod: %.3f| reference_aod: %.3f | relative_difference: %.1f%%"
                % (aod_, reference_aod, rel_diff_aod)
            )

        # Check convergence
        if np.abs(rel_diff_aod) > rel_diff_aod_percentage_threshold:
            if rel_diff_aod > 0:
                if lr_ < 10:
                    run = False
                    print("No convergence. LR goes too low.")
                else:
                    lr_ = lr_ - 1
            else:
                if lr_ > 150:
                    run = False
                    print("No convergence. LR goes too high.")
                else:
                    lr_ = lr_ + 1
        else:
            print("LR found: %f" % lr_)
            run = False
            success = True

        # Check maximum number of iterations
        if iter_ == max_iterations:
            run = False
            print("No convergence. Too many iterations.")

    return lr_, rel_diff_aod, success
