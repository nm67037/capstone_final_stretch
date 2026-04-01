import astropy.units as u
from plasmapy.particles import Particle
from plasmapy.formulary import thermal_speed, plasma_frequency


# 1. Inspect a Particle
# You can use symbols, names, or even LaTeX-like strings
proton = Particle("p+")
#print(f"The mass of a {proton.particle_name} is {proton.mass}")
print(f"The name is {proton.common_name}, the symbol is {proton.symbol}, and the mass is {proton.mass}")

# 2. Set up Plasma Parameters
# You MUST include units using the 'u' object from astropy
temperature = 1e6 * u.K
density = 1e18 * u.m**-3

# 3. Calculate Physics Properties
# PlasmaPy handles all the unit conversions (like K to J) internally
v_th = thermal_speed(temperature, particle="e-")
omega_pe = plasma_frequency(n=density, particle="e-")

print(f"Electron Thermal Speed: {v_th:.2f}")
print(f"Electron Plasma Frequency: {omega_pe:.2e}")

# 4. Units check
# You can easily convert the results to other units
print(f"Thermal Speed in km/s: {v_th.to(u.km / u.s):.2f}")
