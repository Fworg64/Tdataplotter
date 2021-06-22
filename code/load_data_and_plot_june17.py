import loaders

import matplotlib.pyplot as plt
import time
import pdb
from scipy import signal

# load data
samples = [1,2,3]
rates = [2,4,6,8,10]
cap_data_files = {1: {2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-083043.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-083510.txt",
                      6: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-083747.txt",
                      8: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-083935.txt",
                     10: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-084149.txt"},
                  2: {2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-084933.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-085314.txt",
                      6: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-085510.txt",
                      8: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-085709.txt",
                     10: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-085850.txt"},
                  3: {2: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-090536.txt",
                      4: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-090840.txt",
                      6: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-091051.txt",
                      8: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-091243.txt",
                     10: "/home/austinlocal/phd/Tdataplotter/data/cap_files_6_17_21/cap_rec_20210617-091444.txt" }}
load_frame_files   = {1: {2: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/1_2ks/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/1_4ks/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/1_6ks/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/1_8ks/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/1_10ks/specimen.dat"},
                      2: {2: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/2_2ks/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/2_4ks/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/2_6ks/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/2_8ks/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/2_10ks/specimen.dat"},
                      3: {2: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/3_2ks/specimen.dat",
                          4: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/3_4ks/specimen.dat",
                          6: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/3_6ks/specimen.dat",
                          8: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/3_8ks/specimen.dat",
                         10: "/home/austinlocal/phd/Tdataplotter/data/06_17_2021/3_10ks/specimen.dat"}}

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


# generate timebase for cap data

# filter cap data
#b, a = signal.butter(5, .9010)
filtered_cap_data = {}
for sample in samples:
  filtered_sample = {}
  for rate in rates:
    #zi = signal.lfilter_zi(b,a)
    chan_data = [cap["chan_c"] for cap in cap_data[sample][rate]]
    #filtered_sample[rate], _ = signal.lfilter(b,a,chan_data, zi=zi*chan_data[0])
    filtered_sample[rate] = signal.medfilt(chan_data, 75)
  filtered_cap_data[sample]= filtered_sample

# plot cap v time and force v time
print("Plotting Data...")
#pdb.set_trace()
this_time = time.time()
for sample in samples:
  plt.figure(0)
  for rate in rates:
    forces = [point["kN"] for point in force_data[sample][rate]]
    plt.plot(forces[::100])
  plt.legend(["{0} kN/s".format(rate) for rate in rates])
  plt.figure(1)
#  for rate in rates:
#    caps = [point["chan_c"] for point in cap_data[sample][rate]]
#    plt.plot(caps[::100])
  for rate in rates:
    plt.plot(filtered_cap_data[sample][rate][::100])  
  plt.legend(["{0} kN/s filtered".format(rate) for rate in rates])
  plt.ylim([2500,2700])


that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))

plt.show(block=False)
input("Press Enter to close.")
# plot force v cap

# plot force c strain
