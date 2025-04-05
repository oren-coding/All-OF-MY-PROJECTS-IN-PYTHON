c = 299_792_458  # Speed of light in meters per second (m/s)
m = float(input("Enter your mass in kg: "))  # Mass in kilograms

# Energy in joules
E = m * (c ** 2)  

# Convert energy to kilojoules, megajoules, gigajoules, and petajoules
E_kJ = E / 1_000  # Kilojoules
E_MJ = E / 1_000_000  # Megajoules
E_GJ = E / 1_000_000_000  # Gigajoules
E_PJ = E / 1_000_000_000_000_000  # Petajoules

# Real-world energy comparisons
hiroshima_bomb = 63_000_000_000_000  # 63 TJ
one_megaton_tnt = 4.18 * (10**15)  # 4.18 PJ
one_year_usa_power = 3.9 * (10**20)  # 390 EJ

print(f"\nEnergy Calculations for Mass: {m} kg")
print(f"---------------------------------")
print(f"Energy (E) in Joules: {E:.2e} J")
print(f"Energy (E) in Kilojoules: {E_kJ:.2e} kJ")
print(f"Energy (E) in Megajoules: {E_MJ:.2e} MJ")
print(f"Energy (E) in Gigajoules: {E_GJ:.2e} GJ")
print(f"Energy (E) in Petajoules: {E_PJ:.2e} PJ")

print("\nReal-World Comparisons:")
print(f"- Equivalent to {E / hiroshima_bomb:.2f} Hiroshima bombs 💥")
print(f"- Equivalent to {E / one_megaton_tnt:.2f} megatons of TNT 💣")
print(f"- Equivalent to {E / one_year_usa_power:.10f} years of total US power consumption ⚡")

