from src.link_budget import free_space_path_loss


print("VALIDATION CHECKS")
print("-----------------")


# --------------------------------------------------
# Check 1 — Doubling distance
# --------------------------------------------------

frequency_mhz = 1000

fspl_1km = free_space_path_loss(1, frequency_mhz)
fspl_2km = free_space_path_loss(2, frequency_mhz)

distance_difference = fspl_2km - fspl_1km

print("\n1. Doubling distance")
print(f"FSPL at 1 km: {fspl_1km:.2f} dB")
print(f"FSPL at 2 km: {fspl_2km:.2f} dB")
print(f"Difference:   {distance_difference:.2f} dB")

if abs(distance_difference - 6.02) < 0.05:
    print("PASS: Doubling distance adds approximately 6.02 dB.")
else:
    print("FAIL: Unexpected distance relationship.")


# --------------------------------------------------
# Check 2 — Doubling frequency
# --------------------------------------------------

distance_km = 1

fspl_1ghz = free_space_path_loss(distance_km, 1000)
fspl_2ghz = free_space_path_loss(distance_km, 2000)

frequency_difference = fspl_2ghz - fspl_1ghz

print("\n2. Doubling frequency")
print(f"FSPL at 1 GHz: {fspl_1ghz:.2f} dB")
print(f"FSPL at 2 GHz: {fspl_2ghz:.2f} dB")
print(f"Difference:    {frequency_difference:.2f} dB")

if abs(frequency_difference - 6.02) < 0.05:
    print("PASS: Doubling frequency adds approximately 6.02 dB.")
else:
    print("FAIL: Unexpected frequency relationship.")


# --------------------------------------------------
# Check 3 — 3.5 GHz vs 28 GHz
# --------------------------------------------------

fspl_3_5ghz = free_space_path_loss(1, 3500)
fspl_28ghz = free_space_path_loss(1, 28000)

mmwave_difference = fspl_28ghz - fspl_3_5ghz

print("\n3. 3.5 GHz vs 28 GHz")
print(f"FSPL at 3.5 GHz: {fspl_3_5ghz:.2f} dB")
print(f"FSPL at 28 GHz:  {fspl_28ghz:.2f} dB")
print(f"Difference:      {mmwave_difference:.2f} dB")

if abs(mmwave_difference - 18.06) < 0.05:
    print("PASS: Frequency ratio gives expected ~18.06 dB difference.")
else:
    print("FAIL: Unexpected 3.5 GHz vs 28 GHz relationship.")


# --------------------------------------------------
# Final validation summary
# --------------------------------------------------

all_passed = (
    abs(distance_difference - 6.02) < 0.05
    and abs(frequency_difference - 6.02) < 0.05
    and abs(mmwave_difference - 18.06) < 0.05
)

print("\nVALIDATION SUMMARY")
print("------------------")

if all_passed:
    print("ALL CORE VALIDATION CHECKS PASSED")
else:
    print("ONE OR MORE VALIDATION CHECKS FAILED")