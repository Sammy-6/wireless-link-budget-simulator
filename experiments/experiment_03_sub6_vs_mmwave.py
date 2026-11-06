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


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Scenario definitions
# --------------------------------------------------

sub6 = {
    "name": "3.5 GHz Sub-6",
    "frequency_mhz": 3500,
    "transmit_power_dbm": 30,
    "tx_gain_dbi": 10,
    "rx_gain_dbi": 5,
    "system_losses_db": 2,
    "bandwidth_hz": 20e6,
    "noise_figure_db": 5,
    "required_snr_db": 10
}


mmwave = {
    "name": "28 GHz mmWave",
    "frequency_mhz": 28000,
    "transmit_power_dbm": 30,
    "tx_gain_dbi": 24,
    "rx_gain_dbi": 10,
    "system_losses_db": 3,
    "bandwidth_hz": 100e6,
    "noise_figure_db": 7,
    "required_snr_db": 10
}


# --------------------------------------------------
# Distance sweep
# --------------------------------------------------

distance_km = np.linspace(0.05, 20, 700)


# --------------------------------------------------
# Function to evaluate a scenario
# --------------------------------------------------

def evaluate_scenario(scenario):

    path_loss_db = free_space_path_loss(
        distance_km,
        scenario["frequency_mhz"]
    )

    rx_power_dbm = received_power(
        scenario["transmit_power_dbm"],
        scenario["tx_gain_dbi"],
        scenario["rx_gain_dbi"],
        path_loss_db,
        scenario["system_losses_db"]
    )

    noise_dbm = thermal_noise_power(
        scenario["bandwidth_hz"],
        scenario["noise_figure_db"]
    )

    snr_db = calculate_snr(
        rx_power_dbm,
        noise_dbm
    )

    sensitivity_dbm = receiver_sensitivity(
        scenario["bandwidth_hz"],
        scenario["noise_figure_db"],
        scenario["required_snr_db"]
    )

    margin_db = link_margin(
        rx_power_dbm,
        sensitivity_dbm
    )

    viable_indices = np.where(margin_db >= 0)[0]

    if len(viable_indices) > 0:
        max_distance_km = distance_km[viable_indices[-1]]
    else:
        max_distance_km = 0

    return {
        "path_loss_db": path_loss_db,
        "rx_power_dbm": rx_power_dbm,
        "noise_dbm": noise_dbm,
        "snr_db": snr_db,
        "sensitivity_dbm": sensitivity_dbm,
        "margin_db": margin_db,
        "max_distance_km": max_distance_km
    }


# --------------------------------------------------
# Run both scenarios
# --------------------------------------------------

sub6_results = evaluate_scenario(sub6)
mmwave_results = evaluate_scenario(mmwave)


# --------------------------------------------------
# Terminal results
# --------------------------------------------------

print("EXPERIMENT 3 — SUB-6 GHz vs mmWAVE")
print("-----------------------------------")

for scenario, results in [
    (sub6, sub6_results),
    (mmwave, mmwave_results)
]:

    print(f"\n{scenario['name']}")
    print("-" * len(scenario["name"]))

    print(
        f"Bandwidth:            "
        f"{scenario['bandwidth_hz'] / 1e6:.0f} MHz"
    )

    print(
        f"TX antenna gain:      "
        f"{scenario['tx_gain_dbi']:.1f} dBi"
    )

    print(
        f"RX antenna gain:      "
        f"{scenario['rx_gain_dbi']:.1f} dBi"
    )

    print(
        f"Noise power:          "
        f"{results['noise_dbm']:.2f} dBm"
    )

    print(
        f"Receiver sensitivity: "
        f"{results['sensitivity_dbm']:.2f} dBm"
    )

    print(
        f"Max viable distance:  "
        f"{results['max_distance_km']:.2f} km"
    )


# --------------------------------------------------
# Plot 1 — Received power
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    distance_km,
    sub6_results["rx_power_dbm"],
    label=sub6["name"]
)

plt.plot(
    distance_km,
    mmwave_results["rx_power_dbm"],
    label=mmwave["name"]
)

plt.axhline(
    sub6_results["sensitivity_dbm"],
    linestyle="--",
    label="Sub-6 Sensitivity"
)

plt.axhline(
    mmwave_results["sensitivity_dbm"],
    linestyle=":",
    label="mmWave Sensitivity"
)

plt.xlabel("Distance (km)")
plt.ylabel("Received Power (dBm)")
plt.title("Received Power: Sub-6 GHz vs mmWave")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_03_received_power.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# Plot 2 — SNR
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    distance_km,
    sub6_results["snr_db"],
    label=sub6["name"]
)

plt.plot(
    distance_km,
    mmwave_results["snr_db"],
    label=mmwave["name"]
)

plt.axhline(
    10,
    linestyle="--",
    label="Required SNR"
)

plt.xlabel("Distance (km)")
plt.ylabel("SNR (dB)")
plt.title("SNR: Sub-6 GHz vs mmWave")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_03_snr.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# Plot 3 — Link margin
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    distance_km,
    sub6_results["margin_db"],
    label=sub6["name"]
)

plt.plot(
    distance_km,
    mmwave_results["margin_db"],
    label=mmwave["name"]
)

plt.axhline(
    0,
    linestyle="--",
    label="Zero Link Margin"
)

plt.xlabel("Distance (km)")
plt.ylabel("Link Margin (dB)")
plt.title("Link Margin: Sub-6 GHz vs mmWave")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_03_link_margin.png",
    dpi=300
)

plt.show()