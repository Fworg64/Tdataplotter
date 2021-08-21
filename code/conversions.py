from math import pi

def calculate_freq_and_cap(meas, L, Cfilt):
  freqs = [40.0e6 * mea / (2**16) for mea in meas]
  caps  = [1.0 / (L*(2.0*pi*freq)**2) - Cfilt for freq in freqs]
  return freqs, caps


def calculate_drag_force(v1, v2, v3, v4):
  X = -v1 -v2 +v3 +v4
  drag = 15695275 * X + 9088
  return drag