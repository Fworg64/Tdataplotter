import loaders
import conversions

import matplotlib.pyplot as plt
import matplotlib
import time
from scipy import signal
import numpy as np

import pandas as pd

import sys

from scipy.interpolate import interp1d

import pdb

# Set figures
fontsize = 18 
plt.rc('font', size=fontsize, family='sans') 
plt.rc('axes', titlesize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('legend', fontsize=fontsize)

material_rotation_text_deg = 45
mater_color_text_color = 'silver'
mater_color_text_color_air = 'darkgray'



# Load Data
passes  = ["Coal2_New_4thPass_1_0in", "Coal2_New_5thPass_1_0in", 
           "Coal2_New_6thPass_1_5in", "Coal2_New_7thPass_1_0in",
           "Coal4_Worn_1stPass_1_5in","Coal4_Worn_2ndPass_1_5in", 
           "Coal4_Worn_3rdPass_1_5in", "Coal4_Worn_4thPass_1_5in",
           "Coal5_Mod_1stPass_1_5in", "Coal5_Mod_2ndPass_1_5in",
           "Coal5_Worn_4thPass_1_5in", "Coal5_Worn_5thPass_1_5in"]

lines = [1, 2, 3, 4, 5]

chan_name = "chan_b"

good_file_dict = {pass_no: {line_no: False for line_no in lines}
		    for pass_no in passes}

# Note which files are good
good_file_dict["Coal2_New_4thPass_1_0in"][2] = True

good_file_dict["Coal2_New_5thPass_1_0in"][3] = True
good_file_dict["Coal2_New_5thPass_1_0in"][4] = True
good_file_dict["Coal2_New_5thPass_1_0in"][5] = True

good_file_dict["Coal2_New_6thPass_1_5in"][2] = True
good_file_dict["Coal2_New_6thPass_1_5in"][5] = True

good_file_dict["Coal2_New_7thPass_1_0in"][1] = True
good_file_dict["Coal2_New_7thPass_1_0in"][2] = True
good_file_dict["Coal2_New_7thPass_1_0in"][3] = True
good_file_dict["Coal2_New_7thPass_1_0in"][4] = True
good_file_dict["Coal2_New_7thPass_1_0in"][5] = True

good_file_dict["Coal5_Mod_2ndPass_1_5in"][2] = True
good_file_dict["Coal5_Mod_2ndPass_1_5in"][3] = True
good_file_dict["Coal5_Mod_2ndPass_1_5in"][4] = True
good_file_dict["Coal5_Mod_2ndPass_1_5in"][5] = True

good_file_dict["Coal5_Worn_4thPass_1_5in"][2] = True
good_file_dict["Coal5_Worn_4thPass_1_5in"][3] = True
good_file_dict["Coal5_Worn_4thPass_1_5in"][4] = True
good_file_dict["Coal5_Worn_4thPass_1_5in"][5] = True

good_file_dict["Coal5_Worn_5thPass_1_5in"][2] = True

base_path = "/home/austinlocal/phd/Tdataplotter/data/"
cap_base_path_passes_dict = {
    passes[0]: base_path + "cap_files_2_10_23/Niosh-reDAQ/",
    passes[1]: base_path + "cap_files_2_10_23/Niosh-reDAQ/",
    passes[2]: base_path + "cap_files_2_10_23/Niosh-reDAQ/",
    passes[3]: base_path + "cap_files_2_10_23/Niosh-reDAQ/",
    passes[4]: base_path + "cap_files_sept_23/",
    passes[5]: base_path + "September_tests(4and5th)/",
    passes[6]: base_path + "September_tests(4and5th)/",
    passes[7]: base_path + "cap_files_sept_23/",
    passes[8]: base_path + "cap_files_sept_23/",
    passes[9]: base_path + "cap_files_sept_23/",
    passes[10]: base_path + "September_tests(4and5th)/",
    passes[11]: base_path + "September_tests(4and5th)/",
}
lcm_base_path = base_path + "coal/"

cap_passes_dict = { 
    "Coal2_New_4thPass_1_0in": [
#        "cap_rec_20230207-181446.txt", # line 0
        "cap_rec_20230207-182009.txt", # line 1
        "cap_rec_20230207-182359.txt", # line 2
        "cap_rec_20230207-182548.txt", # line 3
        "cap_rec_20230207-183003.txt", # line 4 (sad)
        "cap_rec_20230207-183439.txt", # line 5 (not full line)
        "cap_rec_20230207-183819.txt"], # line 6 (edge) (lost)
    "Coal2_New_5thPass_1_0in": [
        #"cap_rec_20230208-150938.txt", # line 0, # line 1 is lost
        "cap_rec_20230209-134853.txt", # repeat bad line file, # line 1 is lost
        "cap_rec_20230208-161101.txt", # line 2
        "cap_rec_20230208-161400.txt", # line 3
        "cap_rec_20230208-161612.txt", # line 4
        "cap_rec_20230208-161801.txt"], # line 5
    "Coal2_New_6thPass_1_5in": [
#        "cap_rec_20230209-132835.txt",
#        "cap_rec_20230209-134325.txt",
#        "cap_rec_20230209-134454.txt", # line 0 (edge)
#        "cap_rec_20230209-134743.txt",
        "cap_rec_20230209-134853.txt", # line 1 (sad)
#        "cap_rec_20230209-135358.txt",
        "cap_rec_20230209-135436.txt", # line 2
        "cap_rec_20230209-135609.txt", # line 3 (sad)
        "cap_rec_20230209-135744.txt", # line 4 (sad)
        "cap_rec_20230209-142337.txt", # line 5
        "cap_rec_20230209-142629.txt"], # line 6 (edge)
    "Coal2_New_7thPass_1_0in": [
#        "cap_rec_20230209-162217.txt", # line 0 (edge)
#        "cap_rec_20230209-162514.txt",
#        "cap_rec_20230209-162531.txt",
#        "cap_rec_20230209-162621.txt",
        "cap_rec_20230209-162639.txt", # line 1 
        "cap_rec_20230209-162829.txt", # line 2
        "cap_rec_20230209-163002.txt", # line 3
        "cap_rec_20230209-163152.txt", # line 4
        "cap_rec_20230209-163313.txt", # line 5
        "cap_rec_20230209-163554.txt"], # line 6 (edge)
    "Coal4_Worn_1stPass_1_5in": [
        #"cap_rec_20230911-120253.txt", # line 0 (edge)
        "cap_rec_20230911-120423.txt", # line 1
        "cap_rec_20230911-120522.txt", # line 2
        "cap_rec_20230911-122823.txt", # line 3
        "cap_rec_20230911-122912.txt", # line 4
        "cap_rec_20230911-123011.txt", # line 5
        "cap_rec_20230911-123119.txt"], # line 6
    "Coal4_Worn_2ndPass_1_5in": [
        #"cap_rec_20230913-112139.txt", # line 0 (edge)
        "cap_rec_20230913-112655.txt", # line 1
        "cap_rec_20230913-112800.txt", # line 2
        "cap_rec_20230913-112858.txt", # line 3
        "cap_rec_20230913-113250.txt", # line 4
        "cap_rec_20230913-113339.txt", # line 5
        "cap_rec_20230913-113423.txt"], # line 6 (edge)
    "Coal4_Worn_3rdPass_1_5in": [
        #"cap_rec_20230913-115145.txt", # line 0 (edge)
        "cap_rec_20230913-115256.txt", # line 1
        "cap_rec_20230913-115348.txt", # line 2
        "cap_rec_20230913-115454.txt", # line 3
        "cap_rec_20230913-115540.txt", # line 4
        "cap_rec_20230913-115636.txt", # line 5
        "cap_rec_20230913-115743.txt"], # line 6 (edge)
    "Coal4_Worn_4thPass_1_5in": [
        #"cap_rec_20230913-152542.txt", # line 0 (edge)
        "cap_rec_20230913-152756.txt", # line 1
        "cap_rec_20230913-152901.txt", # line 2
        "cap_rec_20230913-152954.txt", # line 3
        "cap_rec_20230913-153038.txt", # line 4
        "cap_rec_20230913-153124.txt", # line 5
        "cap_rec_20230913-153249.txt"], # line 6 (edge)
    "Coal5_Mod_1stPass_1_5in": [
        #"cap_rec_20230927-144103.txt", # line 0 (edge)
        "cap_rec_20230927-144619.txt", # line 1
        "cap_rec_20230927-144839.txt", # line 2
        "cap_rec_20230927-145025.txt", # line 3
        "cap_rec_20230927-145218.txt", # line 4
        "cap_rec_20230927-145218.txt", # line 5
        "cap_rec_20230927-145726.txt"], # line 6 (edge)
    "Coal5_Mod_2ndPass_1_5in": [
        #"cap_rec_20230927-161937.txt", # line 0 (edge)
        "cap_rec_20230927-162400.txt", # line 1
        "cap_rec_20230927-162623.txt", # line 2
        "cap_rec_20230927-162816.txt", # line 3
        "cap_rec_20230927-163026.txt", # line 4
        "cap_rec_20230927-163213.txt", # line 5
        "cap_rec_20230927-163450.txt"], # line 6 (edge)
    "Coal5_Worn_4thPass_1_5in": [
        #"cap_rec_20230929-111957.txt", # line 0 (edge)
        "cap_rec_20230929-112223.txt", # line 1
        "cap_rec_20230929-112411.txt", # line 2
        "cap_rec_20230929-112548.txt", # line 3
        "cap_rec_20230929-112722.txt", # line 4
        "cap_rec_20230929-112905.txt", # line 5
        "cap_rec_20230929-113150.txt"], # line 6 (edge)
    "Coal5_Worn_5thPass_1_5in": [ # Missing files
        "cap_rec_20230929-161222.txt", # line 1
        "cap_rec_20230929-161415.txt", # line 2
        "cap_rec_20230929-161558.txt", # line 3
        "cap_rec_20230929-161758.txt", # line 4
        "cap_rec_20230929-161934.txt"], # line 5
}


cap_data_files = {
    pass_no: {
        inx: cap_base_path_passes_dict[pass_no] + cap_passes_dict[pass_no][inx-1]
        for inx in range(1, len(cap_passes_dict[pass_no]) + 1)}
    for pass_no in passes
}

lcm_data_files = {
    "Coal2_New_4thPass_1_0in": { 0: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-00.lvm",
        1: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-01.lvm",
        2: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-02.lvm",
        3: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-03.lvm",
        4: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-04.lvm",
        5: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-05.lvm",
        6: lcm_base_path + "Coal_2/4th pass/NIOSH-coal-02-07-2023-06.lvm"},
    "Coal2_New_5thPass_1_0in": {  
        1: lcm_base_path + "Coal_2/5th pass/NIOSH-coal-02-08-2023-01.lvm",
        2: lcm_base_path + "Coal_2/5th pass/NIOSH-coal-02-08-2023-02.lvm",
        3: lcm_base_path + "Coal_2/5th pass/NIOSH-coal-02-08-2023-03.lvm",
        4: lcm_base_path + "Coal_2/5th pass/NIOSH-coal-02-08-2023-04.lvm",
        5: lcm_base_path + "Coal_2/5th pass/NIOSH-coal-02-08-2023-05.lvm",
        6: lcm_base_path + "Coal_2/5th pass/NIOSH-coal-02-09-2023-06.lvm"},
    "Coal2_New_6thPass_1_5in": {  0: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-00.lvm",
        1: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-01.lvm",
        2: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-02.lvm",
        3: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-03.lvm",
        4: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-04.lvm",
        5: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-05.lvm",
        6: lcm_base_path + "Coal_2/6th pass/NIOSH-coal-02-09-2023-06.lvm"},
    "Coal2_New_7thPass_1_0in": { 0: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-00.lvm", 
        1: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-01.lvm",
        2: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-02.lvm",
        3: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-03.lvm",
        4: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-04.lvm",
        5: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-05.lvm",
        6: lcm_base_path + "Coal_2/7th pass/NIOSH-coal-02-09-2023-06.lvm"},
    "Coal4_Worn_1stPass_1_5in": { 0: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-0.lvm",
        1: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-1.lvm",
        2: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-2.lvm",
        3: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-3.lvm",
        4: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-4.lvm",
        5: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-5.lvm",
        6: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-6.lvm",
        7: lcm_base_path + "Coal_4/pass 1/Coal4-w-1-7.lvm"},
    "Coal4_Worn_2ndPass_1_5in": { 0: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-0.lvm",
        1: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-1.lvm",
        2: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-2.lvm",
        3: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-3.lvm",
        4: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-4.lvm",
        5: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-5.lvm",
        6: lcm_base_path + "Coal_4/pass 2/Coal4-w-2-6.lvm"},
    "Coal4_Worn_3rdPass_1_5in": { 0: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-0.lvm",
        1: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-1.lvm",
        2: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-2.lvm",
        3: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-3.lvm",
        4: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-4.lvm",
        5: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-5.lvm",
        6: lcm_base_path + "Coal_4/pass 3/Coal4-w-3-6.lvm"},
    "Coal4_Worn_4thPass_1_5in": { 0: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-0.lvm",
        1: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-1.lvm",
        2: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-2.lvm",
        3: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-3.lvm",
        4: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-4.lvm",
        5: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-5.lvm",
        6: lcm_base_path + "Coal_4/pass 4/Coal4-w-4-6.lvm"},
    "Coal5_Mod_1stPass_1_5in": { 0: lcm_base_path + "Coal_5/Pass 1/Coal5-M-0.lvm",
        1: lcm_base_path + "Coal_5/Pass 1/Coal5-M-1.lvm",
        2: lcm_base_path + "Coal_5/Pass 1/Coal5-M-2.lvm",
        3: lcm_base_path + "Coal_5/Pass 1/Coal5-M-3.lvm",
        4: lcm_base_path + "Coal_5/Pass 1/Coal5-M-4.lvm",
        5: lcm_base_path + "Coal_5/Pass 1/Coal5-M-5.lvm",
        6: lcm_base_path + "Coal_5/Pass 1/Coal5-M-6.lvm"},
    "Coal5_Mod_2ndPass_1_5in": { 0: lcm_base_path + "Coal_5/Pass 1/Coal5-M-0.lvm",
        1: lcm_base_path + "Coal_5/Pass 2/Coal5-M-1.lvm",
        2: lcm_base_path + "Coal_5/Pass 2/Coal5-M-2.lvm",
        3: lcm_base_path + "Coal_5/Pass 2/Coal5-M-3.lvm",
        4: lcm_base_path + "Coal_5/Pass 2/Coal5-M-4.lvm",
        5: lcm_base_path + "Coal_5/Pass 2/Coal5-M-5.lvm",
        6: lcm_base_path + "Coal_5/Pass 2/Coal5-M-6.lvm"},
    "Coal5_Worn_4thPass_1_5in": { 0: lcm_base_path + "Coal_5/Pass 4/Coal5-M-0.lvm",
        1: lcm_base_path + "Coal_5/Pass 4/Coal5-M-1.lvm",
        2: lcm_base_path + "Coal_5/Pass 4/Coal5-M-2.lvm",
        3: lcm_base_path + "Coal_5/Pass 4/Coal5-M-3.lvm",
        4: lcm_base_path + "Coal_5/Pass 4/Coal5-M-4.lvm",
        5: lcm_base_path + "Coal_5/Pass 4/Coal5-M-5.lvm",
        6: lcm_base_path + "Coal_5/Pass 4/Coal5-M-6.lvm"},
    "Coal5_Worn_5thPass_1_5in": { 
        1: lcm_base_path + "Coal_5/Pass 5/Coal5-M-1.lvm",
        2: lcm_base_path + "Coal_5/Pass 5/Coal5-M-2.lvm",
        3: lcm_base_path + "Coal_5/Pass 5/Coal5-M-3.lvm",
        4: lcm_base_path + "Coal_5/Pass 5/Coal5-M-4.lvm",
        5: lcm_base_path + "Coal_5/Pass 5/Coal5-M-5.lvm"}
}

print("Loading Data...")
this_time = time.time()
cap_data = {}
lcm_data = {}
cap_dt = 0.002475


force_time_offsets = {
    "Coal2_New_4thPass_1_0in": { 
        1: 1.2,
        2: 1.02,
        3: 1.45,
        4: 0.0, # bad
        5: 1.33},
    "Coal2_New_5thPass_1_0in": { 
        1: 1.2,
        2: 1.07,
        3: 1.7,
        4: 0.83,
        5: 1.25},
    "Coal2_New_6thPass_1_5in": { 
        1: 1.2,
        2: 1.14,
        3: 1.82,
        4: 0.0, # bad
        5: 0.94},
    "Coal2_New_7thPass_1_0in": { 
        1: 1.14,
        2: 1.417,
        3: 1.59,
        4: 1.30,
        5: 1.40},
    "Coal4_Worn_1stPass_1_5in": {
        1: 0.0, # bad
        2: 0.0, # bad
        3: 2.05,
        4: 2.05,
        5: 2.43,
        6: 0.0,
        7: 0.0},
    "Coal4_Worn_2ndPass_1_5in": {
        1: 2.00,
        2: 2.16,
        3: 1.75,
        4: 3.08,
        5: 1.54,
        6: 0.0,
        7: 0.0},
    "Coal4_Worn_3rdPass_1_5in": {
        1: 1.57,
        2: 1.66,
        3: 2.35,
        4: 1.60,
        5: 1.57,
        6: 0.0,
        7: 0.0},
    "Coal4_Worn_4thPass_1_5in": {
        1: 1.57,
        2: 1.12,
        3: 0.9,
        4: 1.08,
        5: 0.93,
        6: 0.0,
        7: 0.0},
    "Coal5_Mod_1stPass_1_5in": {
        1: 1.83,
        2: 0.0, # bad
        3: 0.0, # bad
        4: 0.0,
        5: 0.0,
        6: 0.0,
        7: 0.0},
    "Coal5_Mod_2ndPass_1_5in": {
        1: 1.24,
        2: 1.80 - 0.55,
        3: 2.0,
        4: 1.43,
        5: 1.85,
        6: 0.0,
        7: 0.0},
    "Coal5_Worn_4thPass_1_5in": {
        1: 0.0, # bad
        2: 2.96 - 0.55,
        3: 2.23,
        4: 1.93,
        5: 1.54,
        6: 0.0,
        7: 0.0},
    "Coal5_Worn_5thPass_1_5in": {
        1: 1.57,
        2: 1.54,
        3: 0.0,
        4: 0.0,
        5: 0.0,
        6: 0.0,
        7: 0.0}
}

cap_time_offsets = {
    "Coal2_New_4thPass_1_0in": { 
        1: 18.0,
        2: 20.41,
        3: 18.42,
        4: 0.0, # bad
        5: 20.41},
    "Coal2_New_5thPass_1_0in": { 
        1: 11.4,
        2: 13.86,
        3: 15.53,
        4: 15.78,
        5: 12.06},
    "Coal2_New_6thPass_1_5in": { 
        1: 4.7,
        2: 9.74,
        3: 0.0, # bad
        4: 0.0, # bad
        5: 7.34},
    "Coal2_New_7thPass_1_0in": { 
        1: 2.26, 
        2: 8.85,
        3: 5.8,
        4: 5.06, 
        5: 5.8},
    "Coal4_Worn_1stPass_1_5in": {
        1: 0.0, # bad
        2: 0.0, # bad
        3: 36.28,
        4: 9.22,
        5: 17.34,
        6: 0.0,
        7: 0.0},
    "Coal4_Worn_2ndPass_1_5in": {
        1: 11.14,
        2: 9.45,
        3: 12.36,
        4: 27.06,
        5: 10.10,
        6: 0.0,
        7: 0.0},
    "Coal4_Worn_3rdPass_1_5in": {
        1: 9.72,
        2: 9.68,
        3: 8.86,
        4: 9.49,
        5: 11.0,
        6: 0.0,
        7: 0.0},
    "Coal4_Worn_4thPass_1_5in": {
        1: 27.26,
        2: 35.23,
        3: 17.23,
        4: 9.28,
        5: 12.69,
        6: 0.0,
        7: 0.0},
    "Coal5_Mod_1stPass_1_5in": {
        1: 38.31,
        2: 0.0, # bad
        3: 0.0, # bad
        4: 0.0, # bad
        5: 0.0,
        6: 0.0,
        7: 0.0},
    "Coal5_Mod_2ndPass_1_5in": {
        1: 27.73,
        2: 36.36 - 0.55,
        3: 9.45,
        4: 8.41,
        5: 10.66,
        6: 0.0,
        7: 0.0},
    "Coal5_Worn_4thPass_1_5in": {
        1: 0.0, # bad
        2: 6.82 - 0.55,
        3: 10.28,
        4: 7.34,
        5: 4.94,
        6: 0.0,
        7: 0.0},
    "Coal5_Worn_5thPass_1_5in": {
        1: 10.16,
        2: 6.38,
        3: 0.0, # bad
        4: 0.0, # bad
        5: 0.0,
        6: 0.0,
        7: 0.0}
}
           
plot_duration = 5.5 # seconds

for pass_no in passes:
  cap_data[pass_no] = {}
  lcm_data[pass_no] = {}
  for line in cap_data_files[pass_no].keys():
      # load cap file returns list of dictionaries where each dict is a packet
      cap_data[pass_no][line] = loaders.load_cap_file(cap_data_files[pass_no][line])
      cap_time = 0.0
      for packet in cap_data[pass_no][line]:
        packet["Sec"] = cap_time
        cap_time+= cap_dt
      
  # load lcm data here
  lcm_data[pass_no] = {}
  for line in lcm_data_files[pass_no].keys():
      lcm_data[pass_no][line] = loaders.load_lcm_file(lcm_data_files[pass_no][line])

that_time = time.time()
print("Data loaded in {0} sec".format(that_time - this_time))

print("Plotting Data...")
# Plot all pass_no levels in same plot for one representative sample
# Plot spectrograms if arguments
plot_spec = 1
try:
  plot_spec = int(sys.argv[1])
except IndexError:
  print("Specify the line as the first argument. 1-5")
  print("e.g. $> python3 load_data_and_plot_coal_spring_23.py 1")
  quit()

this_time = time.time()

sub_passes1 = passes[0:4]
sub_passes2 = passes[4:8]
sub_passes3 = passes[8:]

def first_index_greater_than(input_iterable, item):
  try:
    res = next(x for x, val in enumerate(input_iterable) if val > item)
  except StopIteration:
    res = len(input_iterable)
  return res

for plot_passes in [sub_passes1, sub_passes2, sub_passes3]:

  fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)
  if plot_spec > 0 :
    fig2, my_axes = plt.subplots(len(plot_passes),2,sharex=True)

  # Lines #0 and #6 are edge lines, do not have cap data for these
  rep_line = plot_spec

  pass_no_color_list = [(0.05, 0.07, 0.05), 'springgreen', 'darkred', "blue"]
  pass_no_colors = {pass_no:pass_no_color_list[idx] for idx, pass_no in enumerate(plot_passes)}


  # Force data
  force_data_for_csvs = []
  force_plot_handles = []
  for idx,pass_no in enumerate(plot_passes):
    force_values = [conversions.calculate_drag_force_coal(
                      point["v1"], point["v2"], point["v3"], point["v4"])/1000.0
                    for point in lcm_data[pass_no][rep_line]]
    force_times = [point["Sec"]-force_time_offsets[pass_no][rep_line] 
                    for point in lcm_data[pass_no][rep_line]]
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

    # Save data for csv and interp
    force_data_for_csvs.append({"time": force_times[plot_start:plot_end],
                                "values": force_values[plot_start:plot_end]})

  ax1.set_ylabel("Force (kN)")
  #ax1.set_xlabel("Time (s)")
  ax1.set_title("Applied Force vs Time; 1.0 in. pen.")
  ax1.legend()

  # Force data bg fill
  #material_plot_handles = []
  colors_materials = [("white", "Air"), ("slategrey", "Concrete"), ("dimgrey", "Coal")]
  ax1.fill_between(np.arange(0.0, 0.75, 0.01), -2000, 200000, color="white") # air
  ax1.fill_between(np.arange(0.55, 1.5, 0.01), -2000, 200000, color="slategrey")
  ax1.fill_between(np.arange(1.3, 4, 0.01), -2000, 200000, color="dimgrey")
  ax1.fill_between(np.arange(3.85, 5.0, 0.01), -2000, 200000, color="slategrey")

  ax1.set_ylim([-2, 127])
  #ax1.add_artist(pass_no_legend1) # Bring back old legend, display both
  ax1.text(0.2, 50, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)
  ax1.text(0.6, 50, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
  ax1.text(1.3, 50, "Coal", color=mater_color_text_color, rotation = material_rotation_text_deg)
  ax1.text(4.0, 50, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
  ax1.text(5.1, 50, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)

  # Cap data
  cap_data_for_csvs = []
  cap_plot_handles = []
  for idx,pass_no in enumerate(plot_passes):
    had_cap = True
    raw_cap_values = [0.0] * 100
    all_chan_values = {}
    try:
      raw_cap_values  = [point[chan_name]
                    for point in cap_data[pass_no][rep_line]] # these are the encoder values
      
      for cname in ["chan_a", "chan_b", "chan_c", "chan_d"]:
        all_chan_values[cname] = [point[cname]
                  for point in cap_data[pass_no][rep_line]]
          
    except KeyError as e:
      print(pass_no + " has no line #" + str(rep_line))
      had_cap = False
    cap_freqs, cap_values = conversions.calculate_freq_and_cap(raw_cap_values, 18.0e-6, 33.0e-12,2)
    cap_values = np.multiply(cap_values,1.0e12) # convert to pF
    cap_freqs = np.multiply(cap_freqs,1.0e-6) # convert to MHz

    for cname in ["chan_a", "chan_b", "chan_c", "chan_d"]:
        all_chan_values[cname], _ = conversions.calculate_freq_and_cap(all_chan_values[cname], 18.0e-6, 33.0e-12,2)
        all_chan_values[cname] = np.multiply(all_chan_values[cname],1.0e-6) # convert to MHz

    cap_times = [0.0] * 100
    try:
      cap_times   = [point["Sec"]-cap_time_offsets[pass_no][rep_line] 
                    for point in cap_data[pass_no][rep_line]]
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

    # Save data for csv and interp
    cap_data_for_csvs.append({"time": cap_times[plot_start:plot_end],
                              "chan_a": all_chan_values["chan_a"][plot_start:plot_end],
                              "chan_b": all_chan_values["chan_b"][plot_start:plot_end],
                              "chan_c": all_chan_values["chan_c"][plot_start:plot_end],
                              "chan_d": all_chan_values["chan_d"][plot_start:plot_end]
                              })

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
  ax2.set_ylim([1.62, 1.90])
  ax2.invert_yaxis()
  #ax2.legend(handles=cap_material_plot_handles, loc="lower center") # replace with text
  ax2.text(0.2, 1.8, "Air", color=mater_color_text_color_air, rotation = material_rotation_text_deg)
  ax2.text(0.6, 1.8, "Concrete", color=mater_color_text_color, rotation = material_rotation_text_deg)
  ax2.text(1.3, 1.8, "Coal", color=mater_color_text_color, rotation = material_rotation_text_deg)
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
  ax2.legend()

  that_time = time.time()
  print("Data plotted in {0} sec".format(that_time - this_time))


  plt.show(block=False)

  # interp data and save to file
  for idx,pass_no in enumerate(plot_passes):
    # make interp function for force data using cap time base w/ zoh
    force_in_cap_base_func = interp1d(
                                 force_data_for_csvs[idx]["time"], 
                                 force_data_for_csvs[idx]["values"], kind=0,
                                 bounds_error=False,
                                 fill_value=(force_data_for_csvs[idx]["values"][0],
                                             force_data_for_csvs[idx]["values"][-1]))
    file_time_base = cap_data_for_csvs[idx]["time"]
    file_cap_freq_chan_a_vals = cap_data_for_csvs[idx]["chan_a"]
    file_cap_freq_chan_b_vals = cap_data_for_csvs[idx]["chan_b"]
    file_cap_freq_chan_c_vals = cap_data_for_csvs[idx]["chan_c"]
    file_cap_freq_chan_d_vals = cap_data_for_csvs[idx]["chan_d"]
    file_force_vals = force_in_cap_base_func(file_time_base)

    out_np_array = np.array([file_time_base, 
        file_cap_freq_chan_a_vals, 
        file_cap_freq_chan_b_vals, 
        file_cap_freq_chan_c_vals, 
        file_cap_freq_chan_d_vals, 
        file_force_vals]).T

    out_df = pd.DataFrame(out_np_array, columns=["Time (s)", 
             "Freq. A (MHz)", 
             "Freq. B (MHz)", 
             "Freq. C (MHz)", 
             "Freq. D (MHz)", 
             "Force (kN)"])
    filepath = f"coal_csvs/{pass_no}_line_{rep_line}.csv"
    out_df.to_csv(filepath, index=False)

# Save data index file for all files too, not just plotted ones
filenames = []
goodnesses = []
for pass_no in passes:
    for line_no in lines:
        filenames.append(f"{pass_no}_line_{line_no}.csv")
        goodnesses.append(good_file_dict[pass_no][line_no])

index_out_array = np.array([filenames, goodnesses]).T
index_out_df = pd.DataFrame(index_out_array, columns=["Filename", "Data is good"])
index_out_df.to_csv(f"coal_csvs/index.csv", index=False)

input("Press Enter to close")




