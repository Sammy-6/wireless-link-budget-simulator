import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.link_budget import free_space_path_loss


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Frequencies
# --------------------------------------------------

frequencies_mhz = {
    "700 MHz": 700,
    "3.5 GHz": 3500,
    "28 GHz": 28000
}


# --------------------------------------------------
# Distance sweep
# --------------------------------------------------

distance_km = np.linspace(0.1, 25, 500)


# --------------------------------------------------
# Plot path loss for each frequency
# --------------------------------------------------

plt.figure(figsize=(8, 5))

for label, frequency_mhz in frequencies_mhz.items():

    fspl_db = free_space_path_loss(
        distance_km,
        frequency_mhz
    )

    plt.plot(
        distance_km,
        fspl_db,
        label=label
    )


plt.xlabel("Distance (km)")
plt.ylabel("Free-Space Path Loss (dB)")
plt.title("Free-Space Path Loss vs Distance for Different Frequencies")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "experiment_02_frequency_comparison.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# Numerical comparison at selected distances
# --------------------------------------------------

selected_distances = [1, 5, 10, 20]

print("EXPERIMENT 2 — FREQUENCY COMPARISON")
print("-----------------------------------")

for distance in selected_distances:

    print(f"\nDistance: {distance} km")

    for label, frequency_mhz in frequencies_mhz.items():

        fspl_db = free_space_path_loss(
            distance,
            frequency_mhz
        )

        print(
            f"{label:8s}: "
            f"{fspl_db:.2f} dB"
        )


# --------------------------------------------------
# Compare 3.5 GHz and 28 GHz directly
# --------------------------------------------------

fspl_3_5 = free_space_path_loss(
    1,
    3500
)

fspl_28 = free_space_path_loss(
    1,
    28000
)

difference_db = fspl_28 - fspl_3_5

print("\n3.5 GHz vs 28 GHz at 1 km")
print("-------------------------")

print(f"3.5 GHz FSPL: {fspl_3_5:.2f} dB")
print(f"28 GHz FSPL:  {fspl_28:.2f} dB")
print(f"Difference:   {difference_db:.2f} dB")