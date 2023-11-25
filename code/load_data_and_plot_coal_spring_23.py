import loaders
import conversions

import matplotlib.pyplot as plt
import matplotlib
import time
from scipy import signal
import numpy as np

import sys

from scipy.interpolate import interp1d


# Set figures
fontsize = 36
plt.rc('font', size=fontsize, family='sans') 
plt.rc('axes', titlesize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('legend', fontsize=fontsize)

material_rotation_text_deg = 45
mater_color_text_color = 'silver'
mater_color_text_color_air = 'darkgray'



# Load Data
passes  = ["New_4thPass", "New_5thPass", "New_6thPass", "New_7thPass"]
penetrations = ["1.0 in."]
lines        = list(range(0,18))

base_path = "/home/austinlocal/phd/Tdataplotter/data/"
cap_base_path = base_path + "cap_files_2_10_23/Niosh-reDAQ/"
lcm_base_path = base_path + "coal/"

cap_passes_dict = { 
    "New_4thPass": [
#        "cap_rec_20230207-181446.txt",
        "cap_rec_20230207-182009.txt", # line 1
        "cap_rec_20230207-182359.txt", # line 2
        "cap_rec_20230207-182548.txt", # line 3
        "cap_rec_20230207-183003.txt", # line 4 (sad)
        "cap_rec_20230207-183439.txt", # line 5
        "cap_rec_20230207-183819.txt"], # line 6 (edge)
    "New_5thPass": [
        "cap_rec_20230208-150938.txt", # line 1
        "cap_rec_20230208-161101.txt", # line 2
        "cap_rec_20230208-161400.txt", # line 3
        "cap_rec_20230208-161612.txt", # line 4
        "cap_rec_20230208-161801.txt"], # line 5
    "New_6thPass": [
#        "cap_rec_20230209-132835.txt",
#        "cap_rec_20230209-134325.txt",
#        "cap_rec_20230209-134454.txt", # line 0 (edge)
#        "cap_rec_20230209-134743.txt",
        "cap_rec_20230209-134853.txt", # line 1
#        "cap_rec_20230209-135358.txt",
        "cap_rec_20230209-135436.txt", # line 2
        "cap_rec_20230209-135609.txt", # line 3 (sad)
        "cap_rec_20230209-135744.txt", # line 4
        "cap_rec_20230209-142337.txt", # line 5
        "cap_rec_20230209-142629.txt"], # line 6 (edge)
    "New_7thPass": [
#        "cap_rec_20230209-162217.txt", # line 0 (edge)
#        "cap_rec_20230209-162514.txt",
#        "cap_rec_20230209-162531.txt",
#        "cap_rec_20230209-162621.txt",
#        "cap_rec_20230209-162639.txt",
        "cap_rec_20230209-162752.txt", # line 1
        "cap_rec_20230209-162829.txt", # line 2
        "cap_rec_20230209-163002.txt", # line 3
        "cap_rec_20230209-163152.txt", # line 4
        "cap_rec_20230209-163313.txt", # line 5
        "cap_rec_20230209-163554.txt"] # line 6 (edge)
}


cap_data_files = {
    "New_4thPass": {"1.0 in.": { 
        inx: cap_base_path + cap_passes_dict["New_4thPass"][inx-1] 
        for inx in range(1, len(cap_passes_dict["New_4thPass"]) + 1)}},  
    "New_5thPass": {"1.0 in.": { 
        inx: cap_base_path + cap_passes_dict["New_5thPass"][inx-1] 
        for inx in range(1, len(cap_passes_dict["New_5thPass"]) + 1)}},  
    "New_6thPass": {"1.0 in.": { 
        inx: cap_base_path + cap_passes_dict["New_6thPass"][inx-1] 
        for inx in range(1, len(cap_passes_dict["New_6thPass"]) + 1)}},  
    "New_7thPass": {"1.0 in.": { 
        inx: cap_base_path + cap_passes_dict["New_7thPass"][inx-1] 
        for inx in range(1, len(cap_passes_dict["New_7thPass"]) + 1)}}}  


lcm_data_files = {"New_4thPass": {"1.0 in.": { 0: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-00.lvm",
                                       1: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-01.lvm",
                                       2: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-02.lvm",
                                       3: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-03.lvm",
                                       4: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-04.lvm",
                                       5: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-05.lvm",
                                       6: lcm_base_path + "4th pass/NIOSH-coal-02-07-2023-06.lvm"}},
                "New_5thPass": {"1.0 in.": {  
                                       1: lcm_base_path + "5th pass/NIOSH-coal-02-08-2023-01.lvm",
                                       2: lcm_base_path + "5th pass/NIOSH-coal-02-08-2023-02.lvm",
                                       3: lcm_base_path + "5th pass/NIOSH-coal-02-08-2023-03.lvm",
                                       4: lcm_base_path + "5th pass/NIOSH-coal-02-08-2023-04.lvm",
                                       5: lcm_base_path + "5th pass/NIOSH-coal-02-08-2023-05.lvm",
                                       6: lcm_base_path + "5th pass/NIOSH-coal-02-09-2023-06.lvm"}},
                "New_6thPass": {"1.0 in.": {  0: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-00.lvm",
                                       1: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-01.lvm",
                                       2: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-02.lvm",
                                       3: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-03.lvm",
                                       4: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-04.lvm",
                                       5: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-05.lvm",
                                       6: lcm_base_path + "6th pass/NIOSH-coal-02-09-2023-06.lvm"}},
                 "New_7thPass": {"1.0 in.": { 0: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-00.lvm", 
                                        1: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-01.lvm",
                                        2: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-02.lvm",
                                        3: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-03.lvm",
                                        4: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-04.lvm",
                                        5: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-05.lvm",
                                        6: lcm_base_path + "7th pass/NIOSH-coal-02-09-2023-06.lvm"}}}
print("Loading Data...")
this_time = time.time()
cap_data = {}
lcm_data = {}
cap_dt = 0.002475


force_time_offsets = {
    "New_4thPass": { 
        1: 1.2,
        2: 0.8,
        3: 1.2,
        4: 1.3,
        5: 1.2},
    "New_5thPass": { 
        1: 1.2,
        2: 0.8,
        3: 1.2,
        4: 0.9,
        5: 1.2},
    "New_6thPass": { 
        1: 1.2,
        2: 0.8,
        3: 1.2,
        4: 1.3,
        5: 0.7},
    "New_7thPass": { 
        1: 1.2,
        2: 1.2,
        3: 1.5,
        4: 1.1,
        5: 1.4}
}

cap_time_offsets = {
    "New_4thPass": { 
        1: 18.0,
        2: 20.3,
        3: 18.6,
        4: 0.0, # bad
        5: 20.5},
    "New_5thPass": { 
        1: 11.4,
        2: 13.9,
        3: 15.7,
        4: 15.8,
        5: 12.1},
    "New_6thPass": { 
        1: 4.7,
        2: 9.6,
        3: 0.0, # bad
        4: 0.0, # bad
        5: 7.3},
    "New_7thPass": { 
        1: 0.0, # bad
        2: 8.7,
        3: 5.8,
        4: 5.1,
        5: 5.8}
}
           
plot_duration = 5.5 # seconds

for pass_no in passes:
  cap_data[pass_no] = {}
  lcm_data[pass_no] = {}
  for pen in penetrations:
    cap_data[pass_no][pen] = {}
    for line in cap_data_files[pass_no][pen].keys():
      # load cap file returns list of dictionaries where each dict is a packet
      cap_data[pass_no][pen][line] = loaders.load_cap_file(cap_data_files[pass_no][pen][line])
      cap_time = 0.0
      for packet in cap_data[pass_no][pen][line]:
        packet["Sec"] = cap_time
        cap_time+= cap_dt
      
      # load lcm data here
    lcm_data[pass_no][pen] = {}
    for line in lcm_data_files[pass_no][pen].keys():
      lcm_data[pass_no][pen][line] = loaders.load_lcm_file(lcm_data_files[pass_no][pen][line])

that_time = time.time()
print("Data loaded in {0} sec".format(that_time - this_time))

#print("Filtering Data...")

print("Plotting Data...")
# Plot all pass_no levels in same plot for one representative sample
# Plot spectrograms if arguments
plot_spec = int(sys.argv[1])

this_time = time.time()
fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)
if plot_spec > 0 :
  fig2, my_axes = plt.subplots(4,2,sharex=True)

# Just one penetration level for this data set
rep_pen = penetrations[0]
# Lines #0 and #6 are edge lines, do not have cap data for these
rep_line = plot_spec

pass_no_color_list = [(0.2, 0.3, 0.8), 'springgreen', 'darkred', "blue"]
pass_no_colors = {pass_no:pass_no_color_list[idx] for idx, pass_no in enumerate(passes)}

def first_index_greater_than(input_iterable, item):
  try:
    res = next(x for x, val in enumerate(input_iterable) if val > item)
  except StopIteration:
    res = len(input_iterable)
  return res

# Force data
force_plot_handles = []
for idx,pass_no in enumerate(passes):
  force_values = [conversions.calculate_drag_force_coal(
                    point["v1"], point["v2"], point["v3"], point["v4"])/1000.0
                  for point in lcm_data[pass_no][rep_pen][rep_line]]
  force_times = [point["Sec"]-force_time_offsets[pass_no][rep_line] 
                  for point in lcm_data[pass_no][rep_pen][rep_line]]
  plot_start = first_index_greater_than(force_times, 0.0)
  plot_end   = first_index_greater_than(force_times, plot_duration)
  force_plot_handles.append(ax1.plot(force_times[plot_start:plot_end],
                            force_values[plot_start:plot_end],
                            color=pass_no_colors[pass_no], alpha=0.5, 
                            label="{0}".format(pass_no))[0])
  if plot_spec > 0:
    ff, ft, fSxx = signal.spectrogram(np.array(force_values[plot_start:plot_end]), 537.63)#, scaling='density', mode='magnitude')
    my_axes[idx][0].pcolormesh(ft, ff,np.log10(fSxx), shading='gouraud')
    my_axes[idx][0].set_title("Force spec. {0}".format(pass_no))

#pass_no_legend1 = ax1.legend(handles=force_plot_handles, loc="upper right", framealpha=0.5)
ax1.set_ylabel("Force (kN)")
#ax1.set_xlabel("Time (s)")
ax1.set_title("Applied Force vs Time; 1.0 in. pen.")

# Force data bg fill
#material_plot_handles = []
colors_materials = [("white", "Air"), ("slategrey", "Concrete"), ("dimgrey", "Coal")]
#domains = {colors_materials[0] : np.arange(0.0, 0.75, 0.01), 
#           colors_materials[1] : np.arange(0.55, 1.5, 0.01),
#           colors_materials[2] : np.arange(1.3, 4.0, 0.01),
#           colors_materials[1] : np.arange(3.85, 5.0, 0.01),
#           };
#for color_material in colors_materials:
#  material_plot_handles.append(ax1.fill_between(domains[color_material], -2000, 50000,
#                               color=color_material[0], label=color_material[1]))
ax1.fill_between(np.arange(0.0, 0.75, 0.01), -2000, 200000, color="white") # air
ax1.fill_between(np.arange(0.55, 1.5, 0.01), -2000, 200000, color="slategrey")
ax1.fill_between(np.arange(1.3, 4, 0.01), -2000, 200000, color="dimgrey")
ax1.fill_between(np.arange(3.85, 5.0, 0.01), -2000, 200000, color="slategrey")

ax1.set_ylim([-2, 127])
#ax1.add_artist(pass_no_legend1) # Bring back old legend, display both
ax1.text(0.2, 50, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)
ax1.text(0.6, 50, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
ax1.text(2.3, 50, "Coal", color=mater_color_text_color, rotation = material_rotation_text_deg)
ax1.text(4.0, 50, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
ax1.text(5.1, 50, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)

# Cap data
cap_plot_handles = []
for idx,pass_no in enumerate(passes):
  had_cap = True
  raw_cap_values = [0.0] * 100
  try:
    raw_cap_values  = [point["chan_b"] 
                  for point in cap_data[pass_no][rep_pen][rep_line]] # these are the encoder values
  except KeyError as e:
    print(pass_no + " has no line #" + str(rep_line))
    had_cap = False
  cap_freqs, cap_values = conversions.calculate_freq_and_cap(raw_cap_values, 18.0e-6, 33.0e-12,2)
  cap_values = np.multiply(cap_values,1.0e12) # convert to pF
  cap_freqs = np.multiply(cap_freqs,1.0e-6) # convert to MHz

  cap_times = [0.0] * 100
  try:
    cap_times   = [point["Sec"]-cap_time_offsets[pass_no][rep_line] 
                  for point in cap_data[pass_no][rep_pen][rep_line]]
  except KeyError as e:
    print(pass_no + " has no line #" + str(rep_line))
    had_cap = False
  plot_start = first_index_greater_than(cap_times, 0.0)
  plot_end   = first_index_greater_than(cap_times, plot_duration)
  cap_plot_handles.append(ax2.plot(cap_times[plot_start:plot_end],
                                   cap_freqs[plot_start:plot_end],
                                   color=pass_no_colors[pass_no], alpha=0.5,
                                   label=pass_no)[0])
  # Plot Spectrograms
  if plot_spec > 0 and had_cap:
    cf, ct, cSxx = signal.spectrogram(np.array(
                   cap_values[plot_start:plot_end]), 400.00)#, scaling='density', mode='magnitude')
    my_axes[idx][1].pcolormesh(ct, cf, np.log10(cSxx), shading='gouraud')
  my_axes[idx][1].set_title("Cap. spec. {0}".format(pass_no))

#ax3.set_ylabel('Frequency (Hz)')
#ax3.set_xlabel('Time (s)')

#cap_material_plot_handles = []
#for color_material in colors_materials:
#  cap_material_plot_handles.append(ax1.fill_between(domains[color_material], 0, 2000,
#                               color=color_material[0], label=color_material[1]))

#pass_no_legend2 = ax2.legend(handles=cap_plot_handles, loc="upper right", framealpha=0.5)
ax2.set_ylabel("Resonant Freq (MHz)")
ax2.set_xlabel("Time (s)")
ax2.set_title("Sensor Measurements vs Time; 1.0 in. pen.")
ax2.set_ylim([1.72, 1.82])
ax2.invert_yaxis()
#ax2.legend(handles=cap_material_plot_handles, loc="lower center") # replace with text
ax2.text(0.2, 1.8, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)
ax2.text(0.6, 1.8, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
ax2.text(2.3, 1.8, "Coal", color=mater_color_text_color, rotation = material_rotation_text_deg)
ax2.text(4.0, 1.8, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
ax2.text(5.1, 1.8, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)
#ax2.add_artist(pass_no_legend2) # Bring back old legend, display both

ax2.fill_between(np.arange(0.0, 0.75, 0.01), 1.5, 2.0, color="white") # air
ax2.fill_between(np.arange(0.55, 1.5, 0.01), 1.5, 2.0, color="slategrey")
ax2.fill_between(np.arange(1.3, 4, 0.01), 1.5, 2.0, color="dimgrey")
ax2.fill_between(np.arange(3.85, 5.0, 0.01), 1.5, 2.0, color="slategrey")

#for color_material in colors_materials:
#  material_plot_handles.append(ax1.fill_between(domains[color_material], -2000, 10000,
#                               color=color_material[0], label=color_material[1]))
# Set shared x axis
ax2.set_xlim([0,plot_duration ])

that_time = time.time()
print("Data plotted in {0} sec".format(that_time - this_time))

plt.show(block=False)

input("Press Enter to close")


