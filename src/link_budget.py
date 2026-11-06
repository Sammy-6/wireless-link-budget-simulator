import numpy as np


def free_space_path_loss(distance_km, frequency_mhz):
    """
    Calculate free-space path loss in dB.

    Parameters
    ----------
    distance_km : float or array-like
        Distance between transmitter and receiver in kilometres.

    frequency_mhz : float
        Carrier frequency in MHz.

    Returns
    -------
    float or ndarray
        Free-space path loss in dB.
    """

    distance_km = np.asarray(distance_km, dtype=float)

    if np.any(distance_km <= 0):
        raise ValueError("Distance must be greater than zero.")

    if frequency_mhz <= 0:
        raise ValueError("Frequency must be greater than zero.")

    return (
        32.44
        + 20 * np.log10(distance_km)
        + 20 * np.log10(frequency_mhz)
    )


def received_power(
        transmit_power_dbm,
        tx_gain_dbi,
        rx_gain_dbi,
        path_loss_db,
        system_losses_db=0
):
    """
    Calculate received power in dBm.
    """

    return (
        transmit_power_dbm
        + tx_gain_dbi
        + rx_gain_dbi
        - path_loss_db
        - system_losses_db
    )


def thermal_noise_power(bandwidth_hz, noise_figure_db=0):
    """
    Calculate receiver noise power in dBm.

    Uses the approximate thermal noise density:
    -174 dBm/Hz at room temperature.
    """

    if bandwidth_hz <= 0:
        raise ValueError("Bandwidth must be greater than zero.")

    return (
        -174
        + 10 * np.log10(bandwidth_hz)
        + noise_figure_db
    )


def calculate_snr(received_power_dbm, noise_power_dbm):
    """
    Calculate signal-to-noise ratio in dB.
    """

    return received_power_dbm - noise_power_dbm


def receiver_sensitivity(
        bandwidth_hz,
        noise_figure_db,
        required_snr_db
):
    """
    Calculate minimum required receiver power in dBm.
    """

    noise_power_dbm = thermal_noise_power(
        bandwidth_hz,
        noise_figure_db
    )

    return noise_power_dbm + required_snr_db


def link_margin(received_power_dbm, sensitivity_dbm):
    """
    Calculate link margin in dB.

    Positive margin: link is theoretically viable.
    Negative margin: received signal is below sensitivity.
    """

    return received_power_dbm - sensitivity_dbm