import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.link_budget import (
    free_space_path_loss,
    received_power,
    thermal_noise_power,
    calculate_snr,
    receiver_sensitivity,
    link_margin
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# System parameters
# --------------------------------------------------

frequency_mhz = 3500

transmit_power_dbm = 30
tx_gain_dbi = 10
rx_gain_dbi = 5
system_losses_db = 2

bandwidth_hz = 20e6
noise_figure_db = 5
required_snr_db = 10


# --------------------------------------------------
# Distance sweep
# --------------------------------------------------

distance_km = np.linspace(0.1, 25, 500)


# --------------------------------------------------
# Link-budget calculations
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
# Estimate maximum viable distance
# --------------------------------------------------

viable_indices = np.where(margin_db >= 0)[0]

if len(viable_indices) > 0:
    max_viable_distance = distance_km[viable_indices[-1]]
else:
    max_viable_distance = None


print("EXPERIMENT 1 — DISTANCE EFFECTS")
print("--------------------------------")

print(f"Frequency:              {frequency_mhz / 1000:.2f} GHz")
print(f"Receiver sensitivity:   {sensitivity_dbm:.2f} dBm")
print(f"Required SNR:           {required_snr_db:.2f} dB")

if max_viable_distance is not None:
    print(
        f"Approx. maximum distance: "
        f"{max_viable_distance:.2f} km"
    )
else:
    print("No viable distance found.")


# --------------------------------------------------
# Plot 1 — Path loss vs distance
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    distance_km,
    fspl_db
)

plt.xlabel("Distance (km)")
plt.ylabel("Free-Space Path Loss (dB)")
plt.title("Free-Space Path Loss vs Distance at 3.5 GHz")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_01_path_loss_vs_distance.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# Plot 2 — Received power vs distance
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    distance_km,
    rx_power_dbm,
    label="Received Power"
)

plt.axhline(
    sensitivity_dbm,
    linestyle="--",
    label="Receiver Sensitivity"
)

plt.xlabel("Distance (km)")
plt.ylabel("Power (dBm)")
plt.title("Received Power vs Distance at 3.5 GHz")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_01_received_power_vs_distance.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# Plot 3 — SNR vs distance
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    distance_km,
    snr_db,
    label="Available SNR"
)

plt.axhline(
    required_snr_db,
    linestyle="--",
    label="Required SNR"
)

plt.xlabel("Distance (km)")
plt.ylabel("SNR (dB)")
plt.title("SNR vs Distance at 3.5 GHz")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_01_snr_vs_distance.png",
    dpi=300
)

plt.show()