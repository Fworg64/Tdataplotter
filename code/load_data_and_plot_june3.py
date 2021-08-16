import loaders
import conversions

import matplotlib.pyplot as plt
import time
import pdb

from scipy import signal
import numpy as np

# Set figures
fontsize = 18
plt.rc('font', size=fontsize, family='serif')
plt.rc('axes', titlesize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('legend', fontsize=fontsize)

# load data
trials = [1,2,3,4,5]
rates = [2,4,6,8,10]
cap_data_files = {2: {1: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-083817.txt",
                      2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-084110.txt",
                      3: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-084352.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-084617.txt",
                      5: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-084858.txt"},
                  4: {1: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-085227.txt",
                      2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-085435.txt",
                      3: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-085631.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-085849.txt",
                      5: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-090043.txt"},
                  6: {1: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-090310.txt",
                      2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-090455.txt",
                      3: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-090635.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-090813.txt",
                      5: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-090946.txt" },
                  8: {1: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-091150.txt",
                      2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-091326.txt",
                      3: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-091505.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-091650.txt",
                      5: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-091827.txt" },
                 10: {1: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-092045.txt",
                      2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-092353.txt",
                      3: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-092543.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-092716.txt",
                      5: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_3_21/cap_rec_20210603-092900.txt" }}
load_frame_files   = {1: {2: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_1_4kns/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_1_6kns/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_1_8kns/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_1_10kns/specimen.dat"},
                      2: {2: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_2/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_2_4kns/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_2_6kns/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_2_8kns/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_2_10kns/specimen.dat"},
                      3: {2: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_3/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_3_4kns/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_3_6kns/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_3_8kns/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_3_10kns/specimen.dat"},
                      4: {2: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_4/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_4_4kns/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_4_6kns/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_4_8kns/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_4_10kns/specimen.dat"},
                      5: {2: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_5/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_5_4kns/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_5_6kns/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_5_8kns/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_03_2021/T1_6_10kns/specimen.dat"}}

print("Loading Data...")
this_time = time.time()
force_data = {}
cap_data = {}
for rate in rates:
  force_sample_data = {}
  cap_sample_data = {}
  for trial in trials:
    force_sample_data[trial] = loaders.load_frame_file(load_frame_files[trial][rate])
    cap_sample_data[trial] = loaders.load_cap_file(cap_data_files[rate][trial])
  force_data[rate] = force_sample_data
  cap_data[rate] = cap_sample_data
that_time = time.time()
print("Data loaded in {0} sec".format(that_time - this_time))

print("Filtering Data...")
# generate timebase for cap data
cap_dt = 1.0/700.0

for trial in trials:
  for rate in rates:
    cap_time = 0
    for point in cap_data[rate][trial]:
      point["Sec"] = cap_time
      cap_time += cap_dt

# filter cap data
#b, a = signal.butter(5, .9010)
filtered_cap_data = {}
for trial in trials:
  filtered_sample = {}
  for rate in rates:
    #zi = signal.lfilter_zi(b,a)
    chan_data = [cap["chan_a"] for cap in cap_data[rate][trial]]
    #filtered_sample[rate], _ = signal.lfilter(b,a,chan_data, zi=zi*chan_data[0])
    filtered_sample[rate] = signal.medfilt(chan_data, 75)
  filtered_cap_data[trial]= filtered_sample

# convert filtered cap encoder data to freq/cap value
freq_meas = {}
cap_meas  = {}
for trial in trials:
  freq_sample = {}
  cap_sample  = {}
  for rate in rates:
    freq_sample[rate], cap_sample[rate] = \
      conversions.calculate_freq_and_cap(filtered_cap_data[trial][rate], 18.0e-6, 33.0e-12)
  freq_meas[trial] = freq_sample
  cap_meas[trial]  = cap_sample

#pdb.set_trace()

# Generate plots

# plot cap v time and force v time on same plot
print("Plotting Data...")
this_time = time.time()
rate_colors = {2: (0.2, 0.3, 0.8), 4: (0.4, 0.7, 0.6),
               6: (0.6, 0.3, 0.4), 8: (0.8, 0.7, 0.2), 10: (1.0, 0.3, 0.0)}

fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)
for trial in trials:
  for rate in rates:
    forces = [-point["kN"] for point in force_data[rate][trial]]
    times  = [point["Sec"] for point in force_data[rate][trial]]
    ax1.plot(times[::100], forces[::100], color=rate_colors[rate])
  ax1.legend(["{0} kN/s".format(rate) for rate in rates])
  ax1.set_ylabel("Force (kN)")
  ax1.set_title("Applied Force vs Time")

  rate_plot_handle_list = []
  for rate in rates:
    pf_cap = [c/1.0e-12 for c in cap_meas[trial][rate][15:-15:100]]
    times  = [point["Sec"] for point in cap_data[rate][trial][15:-15:100]]
    rate_plot_handle, = ax2.plot(times, pf_cap,
                                 label="{0} kN/s".format(rate), color=rate_colors[rate])
    rate_plot_handle_list.append(rate_plot_handle)

  # Single Legend
  first_legend = ax2.legend(handles=rate_plot_handle_list, loc='upper right')
  ax2.set_ylabel("Capacitance (pF)")
  ax2.set_xlabel("Time (s)")
  ax2.set_title("Measured Cap. vs Time")

'''
  # Split legend
  first_legend = ax2.legend(handles=rate_plot_handle_list[:2], loc='lower center')
  # Add the legend manually to the current Axes.
  plt.gca().add_artist(first_legend)
  # Create another legend for the second set
  ax2.legend(handles=rate_plot_handle_list[2:], loc='lower right')
'''


'''
for rate in rates:
  plt.figure(0)
  for trial in trials:
    forces = [point["kN"] for point in force_data[rate][trial]]
    plt.plot(forces[::100])
  plt.figure()
  for trial in trials:
    pf_cap = [c/1.0e-12 for c in cap_meas[trial][rate][15:-15:100]] 
    plt.plot(pf_cap)
  #plt.ylim([2800,3000])
'''

that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))
plt.show(block=False)
input("Press Enter to close.")
# plot force v cap

# plot force c strain

