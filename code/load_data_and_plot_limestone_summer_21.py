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


lcm_data_files = {"New": {"0.1 in.": { 0: base_path + "lcm_data/New 0.1 inch/line_0.lvm",
                                       1: base_path + "lcm_data/New 0.1 inch/line_1.lvm",
                                       2: base_path + "lcm_data/New 0.1 inch/line_2.lvm",
                                       3: base_path + "lcm_data/New 0.1 inch/line_3.lvm",
                                       4: base_path + "lcm_data/New 0.1 inch/line_4.lvm",
                                       5: base_path + "lcm_data/New 0.1 inch/line_5.lvm",
                                       6: base_path + "lcm_data/New 0.1 inch/line_6.lvm",
                                       7: base_path + "lcm_data/New 0.1 inch/line_7.lvm",
                                       8: base_path + "lcm_data/New 0.1 inch/line_8.lvm",
                                       9: base_path + "lcm_data/New 0.1 inch/line_9.lvm",
                                      10: base_path + "lcm_data/New 0.1 inch/line_10.lvm",
                                      11: base_path + "lcm_data/New 0.1 inch/line_11.lvm",
                                      12: base_path + "lcm_data/New 0.1 inch/line_12.lvm",
                                      13: base_path + "lcm_data/New 0.1 inch/line_13.lvm",
                                      14: base_path + "lcm_data/New 0.1 inch/line_14.lvm",
                                      15: base_path + "lcm_data/New 0.1 inch/line_15.lvm",
                                      16: base_path + "lcm_data/New 0.1 inch/line_16.lvm",
                                      17: base_path + "lcm_data/New 0.1 inch/line_17 (edge).lvm"}},
                "Mod.": {"0.1 in.": {  0: base_path + "lcm_data/MOD 0.1 inch/line_0 (edge).lvm",
                                       1: base_path + "lcm_data/New 0.1 inch/line_1.lvm",
                                       2: base_path + "lcm_data/New 0.1 inch/line_2.lvm",
                                       3: base_path + "lcm_data/New 0.1 inch/line_3.lvm",
                                       4: base_path + "lcm_data/New 0.1 inch/line_4.lvm",
                                       5: base_path + "lcm_data/New 0.1 inch/line_5.lvm",
                                       6: base_path + "lcm_data/New 0.1 inch/line_6.lvm",
                                       7: base_path + "lcm_data/New 0.1 inch/line_7.lvm",
                                       8: base_path + "lcm_data/New 0.1 inch/line_8.lvm",
                                       9: base_path + "lcm_data/New 0.1 inch/line_9.lvm",
                                       10: base_path + "lcm_data/New 0.1 inch/line_10.lvm",
                                       11: base_path + "lcm_data/New 0.1 inch/line_11.lvm",
                                       12: base_path + "lcm_data/New 0.1 inch/line_12.lvm",
                                       13: base_path + "lcm_data/New 0.1 inch/line_13.lvm",
                                       14: base_path + "lcm_data/New 0.1 inch/line_14.lvm",
                                       15: base_path + "lcm_data/New 0.1 inch/line_15.lvm",
                                       16: base_path + "lcm_data/New 0.1 inch/line_16.lvm",
                                       17: base_path + "lcm_data/New 0.1 inch/line_17 (edge).lvm"}}}
#pdb.set_trace()
print("Loading Data...")
this_time = time.time()
cap_data = {}
lcm_data = {}
cap_dt = 1.0/700.0

for wear in wear_levels:
  cap_data[wear] = {}
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
that_time = time.time()
print("Data loaded in {0} sec".format(that_time - this_time))

#print("Filtering Data...")

#pdb.set_trace()
print("Plotting Data...")
this_time = time.time()
fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)

cap_values = [point["chan_c"] for point in cap_data["Mod."]["0.1 in."][3]]
cap_times  = [point["Sec"] for point in cap_data["Mod."]["0.1 in."][13]]

ax2.plot(cap_times[2000:4000], cap_values[2000:4000])
ax2.set_ylim([500, 600])


that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))
plt.show(block=False)
input("Press Enter to close.")





