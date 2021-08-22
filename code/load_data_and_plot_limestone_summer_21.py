import loaders
import conversions

import matplotlib.pyplot as plt
import matplotlib
import time
import pdb
from scipy import signal
import numpy as np

from scipy.interpolate import interp1d

# Set figures
fontsize = 18
plt.rc('font', size=fontsize, family='serif')
plt.rc('axes', titlesize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('legend', fontsize=fontsize)

# Load Data
wear_levels  = ["New", "Mod."]
penetrations = ["0.1 in."]
lines        = list(range(0,18))

base_path = "/home/austinlocal/phd/Tdataplotter/data/limestone/"

cap_data_files = {"New": {"0.1 in.": { 0: base_path + "cap_data/cap_rec_20210727-104758.txt", 
                                       1: base_path + "cap_data/cap_rec_20210727-105453.txt", 
                                       2: base_path + "cap_data/cap_rec_20210727-105732.txt", 
                                       3: base_path + "cap_data/cap_rec_20210727-105900.txt", # lost 4-7 
                                       8: base_path + "cap_data/cap_rec_20210727-110634.txt", 
                                       9: base_path + "cap_data/cap_rec_20210727-110756.txt", 
                                       10: base_path + "cap_data/cap_rec_20210727-110920.txt", 
                                       11: base_path + "cap_data/cap_rec_20210727-111038.txt", 
                                       12: base_path + "cap_data/cap_rec_20210727-111255.txt", 
                                       13: base_path + "cap_data/cap_rec_20210727-111410.txt", 
                                       14: base_path + "cap_data/cap_rec_20210727-111529.txt", 
                                       15: base_path + "cap_data/cap_rec_20210727-111647.txt", 
                                       16: base_path + "cap_data/cap_rec_20210727-111806.txt", 
                                       17: base_path + "cap_data/cap_rec_20210727-114826.txt"}}, 
                 "Mod.": {"0.1 in.": {  0: base_path + "cap_data/cap_rec_20210803-093823.txt",
                                        1: base_path + "cap_data/cap_rec_20210803-094537.txt", 
                                        2: base_path + "cap_data/cap_rec_20210803-094659.txt", 
                                        3: base_path + "cap_data/cap_rec_20210803-094816.txt", 
                                        4: base_path + "cap_data/cap_rec_20210803-094944.txt", 
                                        5: base_path + "cap_data/cap_rec_20210803-095129.txt", 
                                        6: base_path + "cap_data/cap_rec_20210803-095256.txt", 
                                        7: base_path + "cap_data/cap_rec_20210803-095414.txt", 
                                        8: base_path + "cap_data/cap_rec_20210803-095529.txt", 
                                        9: base_path + "cap_data/cap_rec_20210803-095658.txt", 
                                        10: base_path + "cap_data/cap_rec_20210803-095817.txt", 
                                        11: base_path + "cap_data/cap_rec_20210803-095933.txt", 
                                        12: base_path + "cap_data/cap_rec_20210803-100102.txt", 
                                        13: base_path + "cap_data/cap_rec_20210803-100217.txt", 
                                        14: base_path + "cap_data/cap_rec_20210803-100359.txt", 
                                        15: base_path + "cap_data/cap_rec_20210803-100529.txt", 
                                        16: base_path + "cap_data/cap_rec_20210803-100651.txt", 
                                        17: base_path + "cap_data/cap_rec_20210803-102828.txt"}}} 


lcm_data_files = {"New": {"0.1 in.": { 0: base_path + "lcm_data/New 0.1inch/line_0.lvm",
                                       1: base_path + "lcm_data/New 0.1inch/line_1.lvm",
                                       2: base_path + "lcm_data/New 0.1inch/line_2.lvm",
                                       3: base_path + "lcm_data/New 0.1inch/line_3.lvm",
                                       4: base_path + "lcm_data/New 0.1inch/line_4.lvm",
                                       5: base_path + "lcm_data/New 0.1inch/line_5.lvm",
                                       6: base_path + "lcm_data/New 0.1inch/line_6.lvm",
                                       7: base_path + "lcm_data/New 0.1inch/line_7.lvm",
                                       8: base_path + "lcm_data/New 0.1inch/line_8.lvm",
                                       9: base_path + "lcm_data/New 0.1inch/line_9.lvm",
                                      10: base_path + "lcm_data/New 0.1inch/line_10.lvm",
                                      11: base_path + "lcm_data/New 0.1inch/line_11.lvm",
                                      12: base_path + "lcm_data/New 0.1inch/line_12.lvm",
                                      13: base_path + "lcm_data/New 0.1inch/line_13.lvm",
                                      14: base_path + "lcm_data/New 0.1inch/line_14.lvm",
                                      15: base_path + "lcm_data/New 0.1inch/line_15.lvm",
                                      16: base_path + "lcm_data/New 0.1inch/line_16.lvm",
                                      17: base_path + "lcm_data/New 0.1inch/line_17 (edge).lvm"}},
                "Mod.": {"0.1 in.": {  0: base_path + "lcm_data/MOD 0.1inch/line_0 (edge).lvm",
                                       1: base_path + "lcm_data/MOD 0.1inch/line_1.lvm",
                                       2: base_path + "lcm_data/MOD 0.1inch/line_2.lvm",
                                       3: base_path + "lcm_data/MOD 0.1inch/line_3.lvm",
                                       4: base_path + "lcm_data/MOD 0.1inch/line_4.lvm",
                                       5: base_path + "lcm_data/MOD 0.1inch/line_5.lvm",
                                       6: base_path + "lcm_data/MOD 0.1inch/line_6.lvm",
                                       7: base_path + "lcm_data/MOD 0.1inch/line_7.lvm",
                                       8: base_path + "lcm_data/MOD 0.1inch/line_8.lvm",
                                       9: base_path + "lcm_data/MOD 0.1inch/line_9.lvm",
                                       10: base_path + "lcm_data/MOD 0.1inch/line_10.lvm",
                                       11: base_path + "lcm_data/MOD 0.1inch/line_11.lvm",
                                       12: base_path + "lcm_data/MOD 0.1inch/line_12.lvm",
                                       13: base_path + "lcm_data/MOD 0.1inch/line_13.lvm",
                                       14: base_path + "lcm_data/MOD 0.1inch/line_14.lvm",
                                       15: base_path + "lcm_data/MOD 0.1inch/line_15.lvm",
                                       16: base_path + "lcm_data/MOD 0.1inch/line_16.lvm",
                                       17: base_path + "lcm_data/MOD 0.1inch/line_17 (edge).lvm"}}}
#pdb.set_trace()
print("Loading Data...")
this_time = time.time()
cap_data = {}
lcm_data = {}
cap_dt = 0.0025

force_time_offsets = {wear_levels[0]: 1.34, wear_levels[1]: 1.3}
cap_time_offsets =  {wear_levels[0]: 4.65, wear_levels[1]: 7.43}
plot_duration = 5.5 # seconds

for wear in wear_levels:
  cap_data[wear] = {}
  lcm_data[wear] = {}
  for pen in penetrations:
    cap_data[wear][pen] = {}
    for line in cap_data_files[wear][pen].keys():
      # load cap file returns list of dictionaries where each dict is a packet
      cap_data[wear][pen][line] = loaders.load_cap_file(cap_data_files[wear][pen][line])
      cap_time = 0.0
      for packet in cap_data[wear][pen][line]:
        packet["Sec"] = cap_time
        cap_time+= cap_dt
      
      # load lcm data here
    lcm_data[wear][pen] = {}
    for line in lcm_data_files[wear][pen].keys():
      lcm_data[wear][pen][line] = loaders.load_lcm_file(lcm_data_files[wear][pen][line])

that_time = time.time()
print("Data loaded in {0} sec".format(that_time - this_time))

#print("Filtering Data...")

#pdb.set_trace()
print("Plotting Data...")
# Plot all wear levels in same plot for one representative sample
this_time = time.time()
fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)
fig2, my_axes = plt.subplots(2,2,sharex=True)

rep_pen = penetrations[0]
rep_line = 1

wear_colors = {wear_levels[0]: (0.2, 0.3, 0.8), 
               wear_levels[1]: (0.6, 0.3, 0.4),
               #wear_levels[2]: (1.0, 0.3, 0.0)
               }

def first_index_greater_than(input_iterable, item):
  try:
    res = next(x for x, val in enumerate(input_iterable) if val > item)
  except StopIteration:
    res = len(input_iterable)
  return res

for idx,wear in enumerate(wear_levels):
  force_values = [conversions.calculate_drag_force(
                    point["v1"], point["v2"], point["v3"], point["v4"])
                  for point in lcm_data[wear][rep_pen][rep_line]]
  force_times = [point["Sec"]-force_time_offsets[wear] 
                  for point in lcm_data[wear][rep_pen][rep_line]]
  plot_start = first_index_greater_than(force_times, 0.0)
  plot_end   = first_index_greater_than(force_times, plot_duration)
  ax1.plot(force_times[plot_start:plot_end], force_values[plot_start:plot_end],
           color=wear_colors[wear])
  ff, ft, fSxx = signal.spectrogram(np.array(force_values[plot_start:plot_end]), 537.63)
  my_axes[idx][0].pcolormesh(ft, ff, fSxx, shading='gouraud')
  my_axes[idx][0].set_title("Force spec. {0}".format(wear))

ax1.legend(["{0}".format(wear) for wear in wear_levels])
ax1.set_ylabel("Force (lbf)")
#ax1.set_xlabel("Time (s)")
ax1.set_title("Applied Force vs Time; 0.1 in. pen.")

for idx,wear in enumerate(wear_levels):
  cap_values  = [point["chan_b"] 
                  for point in cap_data[wear][rep_pen][rep_line]]
  cap_times   = [point["Sec"]-cap_time_offsets[wear] 
                  for point in cap_data[wear][rep_pen][rep_line]]
  plot_start = first_index_greater_than(cap_times, 0.0)
  plot_end   = first_index_greater_than(cap_times, plot_duration)
  ax2.plot(cap_times[plot_start:plot_end], cap_values[plot_start:plot_end],
           color=wear_colors[wear])
  cf, ct, cSxx = signal.spectrogram(np.array(cap_values[plot_start:plot_end]), 400.00)
  my_axes[idx][1].pcolormesh(ct, cf, cSxx, shading='gouraud')
  my_axes[idx][1].set_title("Cap. spec. {0}".format(wear))

ax2.legend(["{0}".format(wear) for wear in wear_levels])
ax2.set_ylabel("Capacitance (pF)")
ax2.set_xlabel("Time (s)")
ax2.set_title("Measured Cap. vs Time")
ax2.set_ylim([520, 580])

#ax3.set_ylabel('Frequency (Hz)')
#ax3.set_xlabel('Time (s)')

that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))
plt.show(block=False)
input("Press Enter to close.")





