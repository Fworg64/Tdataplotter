import loaders
import conversions

import matplotlib.pyplot as plt
import matplotlib # checked for version
import time
import pdb
from scipy import signal
import numpy as np

from scipy.interpolate import interp1d

# Set figures
fontsize = 22
plt.rc('font', size=fontsize, family='sans')
plt.rc('axes', titlesize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('legend', fontsize=fontsize)

# load data
samples = [1,2]
rates = [2,4,6,8,10]
cap_data_files = {1: {2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-110644.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-110938.txt",
                      6: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-111143.txt",
                      8: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-111320.txt",
                     10: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-111446.txt"},
                  2: {2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-112530.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-112805.txt",
                      6: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-112957.txt",
                      8: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-113136.txt",
                     10: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-113301.txt"},
                  3: {2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-113839.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-114105.txt",
                      6: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-114316.txt",
                      8: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-114428.txt",
                     10: "/home/austinlocal/phd/Tdataplotter/data/cap_files_5_17_22/cap_rec_20220517-114552.txt"}}
load_frame_files   = {1: {2: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/1_2kNs/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/1_4kNs/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/1_6kNs/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/1_8kNs/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/1_10kNs/specimen.dat"},
                      2: {2: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2_2kNs/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2_4kNs/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2_6kNs/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2_8kNs/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2-2_10kNs/specimen.dat"},
                      3: {2: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2-2_2kNs/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2-2_4kNs/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2-2_6kNs/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2-2_8kNs/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/05_17_2022/2-2_10kNs/specimen.dat"}}


print("Loading Data...")
this_time = time.time()
force_data = {}
cap_data = {}
for sample in samples:
  force_sample_data = {}
  cap_sample_data = {}
  for rate in rates:
    force_sample_data[rate] = loaders.load_frame_file(load_frame_files[sample][rate])
    cap_sample_data[rate] = loaders.load_cap_file(cap_data_files[sample][rate])
  force_data[sample] = force_sample_data
  cap_data[sample] = cap_sample_data
that_time = time.time()
print("Data loaded in {0} sec".format(that_time - this_time))

print("Filtering Data...")
# generate timebase for cap data
cap_dt = 1/400.0 #1.0/700.0

for sample in samples:
  for rate in rates:
    cap_time = 0
    for point in cap_data[sample][rate]:
      point["Sec"] = cap_time
      cap_time += cap_dt

# filter cap data
#b, a = signal.butter(5, .9010)
filtered_cap_data = {}
for sample in samples:
  filtered_sample = {}
  for rate in rates:
    #zi = signal.lfilter_zi(b,a)
    chan_data = [cap["chan_b"] for cap in cap_data[sample][rate]]
    filtered_sample[rate] = signal.medfilt(chan_data, 75)
  filtered_cap_data[sample]= filtered_sample

# convert filtered cap encoder data to freq/cap value
freq_meas = {}
cap_meas  = {}
for sample in samples:
  freq_sample = {}
  cap_sample  = {}
  for rate in rates:
    freq_sample[rate], cap_sample[rate] = \
      conversions.calculate_freq_and_cap(filtered_cap_data[sample][rate], 18.0e-6, 33.0e-12)
  freq_meas[sample] = freq_sample
  cap_meas[sample]  = cap_sample


# Generate Plots

# plot cap v time and force v time
print("Plotting Data...")
print('matplotlib: {}'. format(matplotlib. __version__))
#pdb.set_trace()
this_time = time.time()

rate_colors = {2: (0.2, 0.3, 0.8), 4: (0.4, 0.7, 0.6),
               6: (0.6, 0.3, 0.4), 8: (0.8, 0.7, 0.2), 10: (1.0, 0.3, 0.0)}

fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)
for sample in samples:
  for rate in rates:
    forces = [-point["kN"] for point in force_data[sample][rate]]
    times  = [point["Sec"] for point in force_data[sample][rate]]
    ax1.plot(times[::100],forces[::100], color=rate_colors[rate])
  ax1.legend(["{0} kN/s".format(rate) for rate in rates])
  ax1.set_ylabel("Force (kN)")
  #plt.xlabel("Time (s)")
  ax1.set_title("Applied Force vs Time")
#  for rate in rates: # (dont) plot cap raw data
#    caps = [point["chan_c"] for point in cap_data[sample][rate]]
#    plt.plot(caps[::100])
  rate_plot_handle = []
  for rate in rates: # plot median filtered data
    pf_cap = [c/1.0e-12 for c in cap_meas[sample][rate][15:-15:100]] 
    times  = [point["Sec"] for point in cap_data[sample][rate][15:-15:100]]
    rate_plot_handle_, = ax2.plot(times, pf_cap, 
                              label="{0} kN/s".format(rate), color=rate_colors[rate])
    rate_plot_handle.append(rate_plot_handle_)

  # Split legend
  first_legend = ax2.legend(handles=rate_plot_handle[:2], loc='lower center')
  # Add the legend manually to the current Axes.
  plt.gca().add_artist(first_legend)
  # Create another legend for the second set
  ax2.legend(handles=rate_plot_handle[2:], loc='lower right')

  ax2.set_ylabel("Capacitance (pF)")
  ax2.set_xlabel("Time (s)")
  ax2.set_title("Measured Cap. vs Time")
#  plt.ylim([2500,2700])

# plot force v cap
# interpolate force
fig2 = plt.figure()
for sample in samples:
  for rate in rates:
    forces = [-point["kN"] for point in force_data[sample][rate]]
    force_times = [point["Sec"] for point in force_data[sample][rate]]
    interp_func = interp1d(force_times, forces,  bounds_error=False, fill_value=0.0)
    pf_cap = [c/1.0e-12 for c in cap_meas[sample][rate][15:-15:100]] 
    cap_times  = [point["Sec"] for point in cap_data[sample][rate][15:-15:100]]
    interp_forces = interp_func(cap_times)
    plt.plot(pf_cap, interp_forces, color=rate_colors[rate])
plt.legend(["{0} kN/s".format(rate) for rate in rates])
plt.xlabel('Capacitance (pF)')
plt.ylabel("Force (kN)")
plt.title("Force vs Capacitance")

# plot device strain
fig3 = plt.figure()
for sample in samples:
  for rate in rates:
    dists = [-(point["mm"]+25.45) for point in force_data[sample][rate]] # subtract offset and flip
    dists = np.multiply(dists,3.0/5.0) # load frame is roughly 1.5 times stiffer than sensor
    strains = np.multiply(dists,1.0/1.8288) # divide by height for strain
    dist_times = [point["Sec"] for point in force_data[sample][rate]]
    plt.plot(dist_times, strains, color=rate_colors[rate])
plt.legend(["{0} kN/s".format(rate) for rate in rates])
plt.xlabel('Time (s)')
plt.ylabel(r'Strain $(\Delta \ell / \ell_0)$')
plt.title("Device Strain vs Time")


that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))
plt.show(block=False)
input("Press Enter to close.")
