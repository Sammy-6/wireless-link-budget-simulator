import pandas as pd
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


scenarios = [
    {
        "Scenario": "3.5 GHz Sub-6",
        "Distance_km": 1,
        "Frequency_MHz": 3500,
        "Transmit_Power_dBm": 30,
        "TX_Gain_dBi": 10,
        "RX_Gain_dBi": 5,
        "System_Loss_dB": 2,
        "Bandwidth_Hz": 20e6,
        "Noise_Figure_dB": 5,
        "Required_SNR_dB": 10
    },
    {
        "Scenario": "28 GHz mmWave",
        "Distance_km": 1,
        "Frequency_MHz": 28000,
        "Transmit_Power_dBm": 30,
        "TX_Gain_dBi": 24,
        "RX_Gain_dBi": 10,
        "System_Loss_dB": 3,
        "Bandwidth_Hz": 100e6,
        "Noise_Figure_dB": 7,
        "Required_SNR_dB": 10
    },
    {
        "Scenario": "12 GHz LEO",
        "Distance_km": 550,
        "Frequency_MHz": 12000,
        "Transmit_Power_dBm": 30,
        "TX_Gain_dBi": 30,
        "RX_Gain_dBi": 35,
        "System_Loss_dB": 3,
        "Bandwidth_Hz": 100e6,
        "Noise_Figure_dB": 2,
        "Required_SNR_dB": 8
    }
]


results = []

for s in scenarios:

    fspl_db = free_space_path_loss(
        s["Distance_km"],
        s["Frequency_MHz"]
    )

    rx_power_dbm = received_power(
        s["Transmit_Power_dBm"],
        s["TX_Gain_dBi"],
        s["RX_Gain_dBi"],
        fspl_db,
        s["System_Loss_dB"]
    )

    noise_dbm = thermal_noise_power(
        s["Bandwidth_Hz"],
        s["Noise_Figure_dB"]
    )

    snr_db = calculate_snr(
        rx_power_dbm,
        noise_dbm
    )

    sensitivity_dbm = receiver_sensitivity(
        s["Bandwidth_Hz"],
        s["Noise_Figure_dB"],
        s["Required_SNR_dB"]
    )

    margin_db = link_margin(
        rx_power_dbm,
        sensitivity_dbm
    )

    results.append({
        "Scenario": s["Scenario"],
        "Distance (km)": s["Distance_km"],
        "Frequency (GHz)": s["Frequency_MHz"] / 1000,
        "Bandwidth (MHz)": s["Bandwidth_Hz"] / 1e6,
        "FSPL (dB)": round(fspl_db, 2),
        "Received Power (dBm)": round(rx_power_dbm, 2),
        "Noise Power (dBm)": round(noise_dbm, 2),
        "SNR (dB)": round(snr_db, 2),
        "Sensitivity (dBm)": round(sensitivity_dbm, 2),
        "Link Margin (dB)": round(margin_db, 2),
        "Status": "VIABLE" if margin_db >= 0 else "NOT VIABLE"
    })


df = pd.DataFrame(results)

print("\nFINAL SCENARIO COMPARISON")
print("-------------------------")
print(df.to_string(index=False))


output_file = RESULTS_DIR / "final_scenario_comparison.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    f"\nSaved comparison table to:\n{output_file}"
)