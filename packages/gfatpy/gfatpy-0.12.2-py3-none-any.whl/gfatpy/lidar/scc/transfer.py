

from pdb import set_trace
from typing import Tuple
from gfatpy.lidar.scc import scc_access
from gfatpy.lidar.scc import SCC_INFO

SCC_SERVER_SETTINGS = SCC_INFO["server_settings"]

def check_scc_connection() -> bool: 
    """ Check if SCC server is available. """

    scc_obj = scc_access.SCC(
        tuple(SCC_SERVER_SETTINGS["basic_credentials"]),
        None,
        SCC_SERVER_SETTINGS["base_url"],
    )

    connection = scc_obj.login(SCC_SERVER_SETTINGS["website_credentials"])
    check_connection = connection.status_code == 200
    if not check_connection:
        raise Exception("Connection to SCC server failed.")
    else:
        scc_obj.logout()

    return check_connection

def check_measurement_id_in_scc(measurement: str) -> Tuple[bool, scc_access.Measurement | None]:
    """ Check if a measurement is already in SCC. """

    if len(measurement) != 15:
        raise ValueError("Measurement ID must have 14 characters.")

    scc_obj = scc_access.SCC(
        tuple(SCC_SERVER_SETTINGS["basic_credentials"]),
        None,
        SCC_SERVER_SETTINGS["base_url"],
    )

    scc_obj.login(SCC_SERVER_SETTINGS["website_credentials"])
    
    try:
        meas_obj, status = scc_obj.get_measurement(measurement)
        measurement_id_in_scc = meas_obj is not None        
    except Exception as e:
        meas_obj = None
        number = int(str(e).split("Status code ")[-1][:-1])
        scc_obj.logout()
        raise ValueError(f"Error code: {number}")
    scc_obj.logout()

    return measurement_id_in_scc, meas_obj
