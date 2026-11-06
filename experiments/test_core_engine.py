from src.link_budget import (
    free_space_path_loss,
    received_power,
    thermal_noise_power,
    calculate_snr,
    receiver_sensitivity,
    link_margin
)


# -------------------------
# Test scenario
# -------------------------

distance_km = 1
frequency_mhz = 3500

transmit_power_dbm = 30
tx_gain_dbi = 10
rx_gain_dbi = 5

system_losses_db = 2

bandwidth_hz = 20e6
noise_figure_db = 5

required_snr_db = 10


# -------------------------
# Calculations
# -------------------------

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


# -------------------------
# Results
# -------------------------

print("WIRELESS LINK BUDGET TEST")
print("-------------------------")

print(f"Distance:            {distance_km:.2f} km")
print(f"Frequency:           {frequency_mhz / 1000:.2f} GHz")
print(f"Free-space loss:     {fspl_db:.2f} dB")

print()

print(f"Received power:      {rx_power_dbm:.2f} dBm")
print(f"Noise power:         {noise_dbm:.2f} dBm")
print(f"SNR:                 {snr_db:.2f} dB")

print()

print(f"Receiver sensitivity:{sensitivity_dbm:.2f} dBm")
print(f"Link margin:         {margin_db:.2f} dB")

print()

if margin_db > 0:
    print("Link status: VIABLE")
elif margin_db == 0:
    print("Link status: AT THRESHOLD")
else:
    print("Link status: NOT VIABLE")