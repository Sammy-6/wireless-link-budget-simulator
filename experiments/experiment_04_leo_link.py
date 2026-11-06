from src.link_budget import (
    free_space_path_loss,
    received_power,
    thermal_noise_power,
    calculate_snr,
    receiver_sensitivity,
    link_margin
)


# --------------------------------------------------
# Simplified illustrative LEO downlink scenario
# --------------------------------------------------

distance_km = 550
frequency_mhz = 12000

transmit_power_dbm = 30
tx_gain_dbi = 30
rx_gain_dbi = 35

system_losses_db = 3

bandwidth_hz = 100e6
noise_figure_db = 2
required_snr_db = 8


# --------------------------------------------------
# Calculations
# --------------------------------------------------

fspl_db = free_space_path_loss(
    distance_km,
    frequency_mhz
)

rx_power_dbm = received_power(
    transmit_power_dbm,
    tx_gain_dbi,
    rx_gain_dbi,
    fspl_db,
    system_losses_db
)

noise_dbm = thermal_noise_power(
    bandwidth_hz,
    noise_figure_db
)

snr_db = calculate_snr(
    rx_power_dbm,
    noise_dbm
)

sensitivity_dbm = receiver_sensitivity(
    bandwidth_hz,
    noise_figure_db,
    required_snr_db
)

margin_db = link_margin(
    rx_power_dbm,
    sensitivity_dbm
)


# --------------------------------------------------
# Results
# --------------------------------------------------

print("EXPERIMENT 4 — SIMPLIFIED LEO SATELLITE LINK")
print("--------------------------------------------")

print(f"Link distance:         {distance_km:.0f} km")
print(f"Frequency:             {frequency_mhz / 1000:.2f} GHz")

print()

print(f"Transmit power:        {transmit_power_dbm:.2f} dBm")
print(f"TX antenna gain:       {tx_gain_dbi:.2f} dBi")
print(f"RX antenna gain:       {rx_gain_dbi:.2f} dBi")
print(f"System losses:         {system_losses_db:.2f} dB")

print()

print(f"Free-space path loss:  {fspl_db:.2f} dB")
print(f"Received power:        {rx_power_dbm:.2f} dBm")
print(f"Noise power:           {noise_dbm:.2f} dBm")
print(f"SNR:                   {snr_db:.2f} dB")

print()

print(f"Receiver sensitivity:  {sensitivity_dbm:.2f} dBm")
print(f"Link margin:           {margin_db:.2f} dB")

print()

if margin_db > 0:
    print("Link status: VIABLE")
elif margin_db == 0:
    print("Link status: AT THRESHOLD")
else:
    print("Link status: NOT VIABLE")