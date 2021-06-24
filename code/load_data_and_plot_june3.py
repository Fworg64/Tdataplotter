import loaders
import conversions

import matplotlib.pyplot as plt
import time
import pdb

from scipy import signal
import numpy as np

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
    chan_data = [cap["chan_c"] for cap in cap_data[rate][trial]]
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
# plot cap v time and force v time
print("Plotting Data...")
this_time = time.time()
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


that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))
plt.show(block=False)
input("Press Enter to close.")
# plot force v cap

# plot force c strain

