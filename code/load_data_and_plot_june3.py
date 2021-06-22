import loaders

import matplotlib.pyplot as plt
import time
import pdb

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
# generate timebase for cap data

#pdb.set_trace()
# plot cap v time and force v time
print("Plotting Data...")
this_time = time.time()
for trial in trials:
  plt.figure()
  for rate in rates:
    forces = [point["kN"] for point in force_data[rate][trial]]
    plt.plot(forces[::100])
  plt.figure()
  for rate in rates:
    caps = [point["chan_c"] for point in cap_data[rate][trial]]
    plt.plot(caps[::100])
  plt.ylim([2800,3000])


that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))

plt.show()
# plot force v cap

# plot force c strain

