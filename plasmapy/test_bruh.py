import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from plasmapy.formulary import ExB_drift, gyrofrequency
from plasmapy.particles import Particle
from plasmapy.plasma.grids import CartesianGrid
from plasmapy.simulation.particle_tracker.particle_tracker import ParticleTracker
from plasmapy.simulation.particle_tracker.save_routines import IntervalSaveRoutine
from plasmapy.simulation.particle_tracker.termination_conditions import (
    TimeElapsedTerminationCondition,
)
