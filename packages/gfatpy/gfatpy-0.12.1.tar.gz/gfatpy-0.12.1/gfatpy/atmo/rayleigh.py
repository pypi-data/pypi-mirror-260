from pdb import set_trace
from typing import Any
import numpy as np
import math
import xarray as xr
from pandas.core.arrays import ExtensionArray
from scipy.constants import physical_constants
from gfatpy.atmo.atmo import attenuated_backscatter, transmittance
from gfatpy.atmo.freudenthaler_molecular_properties import molecular_depolarization, f_kbwt, f_kbwc


def retrieve_molecular_extinction_and_backscatter(
    r: np.ndarray[float],
    temperature: np.ndarray[float],
    pressure: np.ndarray[float],
    wavelength: float,
    component: str = "ideal",  
) -> tuple[np.ndarray[np.float64], np.ndarray[np.float64], np.ndarray[np.float64]]:
    """Extracted from rayextv2.m from Adolfo Comeron code
       Function that gets as input the altitude in [m], the temperature in [K], the pressure in [Pa], the wavelength in [nm] and
       the mode_standard (0 for non-standard and 1 for standard atmosphere) and returns the Rayleigh extinction [m-1], the Rayleigh backscatter [m-1sr-1] and the N concentration [molecules/km3].

       % RAYLEIGH EXTINCTION using the King factor [km-1]
       % See: Bodhaine et al. "On Rayleigh Optical Depth Calculations"

    Args:
        r (np.ndarray[np.float64]): altitude array [m]
        temperature (float | np.ndarray[float]): floor-level temperature or temperature profile [K]. If isinstance(temperature, float), standard atmosphere is used.
        pressure (float | np.ndarray[float]): floor-level pressure or pressure profile [Pa]. If isinstance(pressure, float), standard atmosphere is used.
        wavelength (float): wavelength [nm]

    Returns:
        tuple[np.ndarray[np.float64], np.ndarray[np.float64], np.float64]: alfasca: Rayleigh extinction [m-1], betasca: Rayleigh backscatter [m-1sr-1], molecular_lidar_ratio: molecular lidar ratio [sr]

    """                

    # Input units: r [m], T0 [Kelvin], P0 [Pa], lambda [nm]
    # Conversion to the units of this function:
    r = (r / 1e3).astype(np.float64)  # Convert altitude to [km]
    # Altitude is in m, eventhough they say it should be in km

    # Tab.1, p.1857. Constituents and mean molecular weight of dry air.
    # Pressure P [mb], Temperature T [K]
    # These computations are not necessary except for computation
    # of the optical depth tau(z-->inf) in eq.(25).
    # Nombre de mols de nitrogen.
    # pressure_to_temperature =  pressure / temperature
    # n1 = (78.084e-2 / R) * pressure_to_temperature  
    # # Nombre de mols d'Oxigen.
    # n2 = (20.946e-2 / R) * pressure_to_temperature
    # # Nombre de mols d'Argó.
    # n3 = (0.934e-2 / R) * pressure_to_temperature
    # # Nombre de mols de Neó.
    # n4 = (1.818e-5 / R) * pressure_to_temperature
    # # Nombre de mols d'Heli.
    # n5 = (5.24e-6 / R) * pressure_to_temperature
    # # Nombre de mols de Kriptó.
    # n6 = (1.14e-6 / R) * pressure_to_temperature
    # # Nombre de mols d'Hidrogen.
    # n7 = (5.80e-7 / R) * pressure_to_temperature
    # # Nombre de mols de Xenó.
    # n8 = (9.00e-8 / R) * pressure_to_temperature
    # # Nombre de mols de CO2 (360 ppm_vol for standard air.)
    # n9 = (0.0360e-2 / R) * pressure_to_temperature
    # # Nombre de mols de CH4.
    # n10 = (1.6e-6 / R) * pressure_to_temperature
    # # Nombre de mols de NO2;
    # n11 = (5e-7 / R) * pressure_to_temperature
    # ng = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8 + n9 + n10 + n11  # [mol/m3]
    # pressure = (pressure / 100)
    pressure = (pressure / 100).astype(np.float64)  # Convert pressure to [mb]
    temperature = temperature.astype(np.float64)  # Convert temperature to [K]
    NA = physical_constants["Avogadro constant"][0]  # [mol-1]
    Ns = np.array(NA / 22.4141 * 273.15 / 1013.25 * 1e3 *(pressure / temperature), dtype=np.float64) # [molecules/m3] P[mb], T[K] #Convert to float64 to avoid overflow error in Ns**2
    # Ns=2.546899e19 mol/cm3 at 288.15 K, 1013.25 mb. See. p.1857, eq.22
    # Ns=ng*NA;		# If activated, you get the same result as above because ng=100*(P./T);
        
    # COMPUTE RAYLEIGH EXTINCTION [km-1]. Eq.(22)-(23)
    lab = wavelength * 1e-3

    # Refractive index. Eq.(21) given at 288.15 K, 1013.25 mb, 360 ppm CO2
    n = 1 + pressure / 1013.25 * 288.15 / temperature * 1e-8 * (
        8060.77 + 2481070 / (132.274 - lab ** (-2)) + 17456.3 / (39.32957 - lab ** (-2))
    )

    # F-factor or King Factor. Eq.(23)(5)(6)
    kingf = (
        78.084 * (1.034 + 3.17e-4 / lab**2)
        + 20.946 * (1.096 + 1.385e-3 / lab**2 + 1.448e-4 / lab**4)
        + 0.934 * 1.00
        + 0.036 * 1.15
    ) / (78.084 + 20.946 + 0.934 + 0.036)

    # Scattering cross section [m2/molecule]
    sigma = (
        8
        * math.pi**3
        * (n**2 - 1) ** 2
        / (3 * (wavelength * 1e-9) ** 4 * Ns**2)
        * kingf
    )
    sigma = 8 * math.pi ** 3 * (n ** 2 - 1) ** 2 / (3 * (wavelength * 1e-9) ** 4 * Ns**2) * kingf
    # sigma=24*pi^3*(n.^2-1).^2./((n.^2+2).^2*(lambda*1e-9)^4.*Ns.^2)*kingf;

    if component == "total":
        lr_function = f_kbwt
    elif component == "cabannes":
        lr_function = f_kbwc
    elif component == "ideal":
        lr_function = lambda x: 1.0
    else:
        raise ValueError(f"{component} not found.")
    molecular_lidar_ratio = (8.*np.pi/3.) * lr_function(wavelength)
    
    # Extinction [m-1]
    alfasca = sigma * Ns
    # betasca = alfasca / 8.37758041 #From Adolfo's code
    betasca = alfasca / molecular_lidar_ratio
    
    # N en molecules/Km^3.
    # N2_concentration = n1 * 6.0221367e23 * 1e9
    # save rayext

    # % OUTPUTS:
    # % alfasca:	Rayleigh extinction [km-1]
    # % betasca:	Rayleigh backscatter [km-1sr-1]
    # % N:	N2 concentration [molecules/km3]

    # Conversion of output into SI units:    
    # alfasca = alfasca / 1000  # [m-1]
    # betasca = betasca / 1000  # [m-1sr-1]    
    return alfasca, betasca, molecular_lidar_ratio

def molecular_properties(
    wavelength: float,
    pressure: np.ndarray[Any, np.dtype[np.float64]] | ExtensionArray,
    temperature: np.ndarray[Any, np.dtype[np.float64]] | ExtensionArray,
    heights: np.ndarray[Any, np.dtype[np.float64]] | ExtensionArray,
    times: np.ndarray[Any, np.dtype[np.float64]] | None = None,
    component: str = "ideal",
) -> xr.Dataset:
    """Molecular Attenuated  Backscatter: beta_mol_att = beta_mol * Transmittance**2

    Args:
        wavelength (float): wavelength of our desired beta molecular attenuated
        pressure (np.ndarray[Any, np.dtype[np.float64]]): pressure profile
        temperature (np.ndarray[Any, np.dtype[np.float64]]): temperature profile
        heights (np.ndarray[Any, np.dtype[np.float64]]): height profile
        times (np.ndarray[Any, np.dtype[np.float64]] | None, optional): time array. Defaults to None. Note: this is not used in the calculation yet. In development.
        component (str, optional): _description_. Defaults to "ideal".

    Returns:
        xr.Dataset: molecular attenuated backscatter profile, molecular backscatter profile, molecular extinction profile, molecular lidar ratio, molecular depolarization ratio
    """

    # molecular backscatter and extinction #
    molecular_extinction, molecular_backscatter, molecular_lidar_ratio = retrieve_molecular_extinction_and_backscatter(heights, temperature, pressure, wavelength, component=component)
    
    #TODO: molecular depolarization ratio defined as ideal? 
    molecular_depolarization_ratio = molecular_depolarization(wavelength, component='cabannes')

    if times is None:
        mol_properties = xr.Dataset(
            {
                "molecular_beta": (["range"], molecular_backscatter),
                "molecular_alpha": (["range"], molecular_extinction),
                "molecular_lidar_ratio": ([], molecular_lidar_ratio),
                "molecular_depolarization": ([], molecular_lidar_ratio),
            },
            coords={"range": heights},
        )
    else:
        mol_properties = xr.Dataset(
            {
                "molecular_beta": (["time", "range"], molecular_backscatter),
                "molecular_alpha": (["time", "range"], molecular_extinction),                
                "molecular_lidar_ratio": (["time"], molecular_lidar_ratio),
                "molecular_depolarization": (["time"], molecular_depolarization_ratio)
            },
            coords={
                "time": times,
                "range": heights,
            },  # FIXME: time is not used in the calculation yet
        )
    return mol_properties