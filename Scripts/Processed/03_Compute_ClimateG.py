import os
import numpy as np
import metview as mv

#############################################################################
# CODE DESCRIPTION
# 03_Compute_ClimateG.py merges the climatologies for each sub-area, and creates a 
# global field.
# Code runtime: the code takes up to 1 minute to run in serial.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (integer, in hours): rainfall accumulation period.
# NumSA (integer): number of total considered sub-areas.
# SystemFC (string): forecasting system to consider.
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory containing ERA5.
# DirOUT (string): relative path for the output directory containing the climatology.

# INPUT PARAMETERS
Acc = 24
NumSA = 160
SystemFC = "ERA5"
GitRepo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/RainThr_4FlashFloodFC_ecPointERA5"
FileIN_Sample_Grib_Global = "Data/Raw/Sample_Grib_Global.grib"
DirIN = "Data/Compute/02_ClimateSA"
DirOUT = "Data/Compute/03_ClimateG"
#############################################################################


# Reading the global field for the sample grib
sample_grib_global = mv.read(GitRepo + "/" + FileIN_Sample_Grib_Global)
NumGP_g = int(mv.count(mv.values(sample_grib_global)))
NumGP_sa = int(NumGP_g / NumSA)

# Merging the climatologies for all the sub-areas to create global fields
print("Merging the climatologies for all the sub-areas to create global fields")
print(" - Reading the sub-area n." + str(0) + "/" + str(NumSA))
DirIN_temp = GitRepo + "/" + DirIN + "_" + f'{Acc:02d}' + "h/" + SystemFC
FileIN_temp = "ClimateSA_" + f'{0:03d}' + ".npy"
tp_G = np.load(DirIN_temp + "/" + FileIN_temp)
npercs = tp_G.shape[1]
for ind_SA in range(1,NumSA):
      print(" - Reading the sub-area n." + str(ind_SA) + "/" + str(NumSA-1))
      DirIN_temp = GitRepo + "/" + DirIN + "_" + f'{Acc:02d}' + "h/" + SystemFC
      FileIN_temp = "ClimateSA_" + f'{ind_SA:03d}' + ".npy"
      tp_SA = np.load(DirIN_temp + "/" + FileIN_temp)
      tp_G = np.concatenate((tp_G, tp_SA), axis=0) 

#  Storing the percentiles as grib
print("Converting the numpy array into grib")
percs_tot_global = None
for ind_perc in range(npercs):
      print(" - Merging percentile n." + str(ind_perc) + "/" + str(npercs))
      percs_tot_global = mv.merge(percs_tot_global, mv.set_values(sample_grib_global, tp_G[:,ind_perc]))

# Saving the output file
print("Storing the output file")
DirOUT_temp = GitRepo + "/" + DirOUT  + "_" + f'{Acc:02d}' + "h/" + SystemFC 
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
FileOUT = DirOUT_temp + "/Climate_" + SystemFC + "_" + f'{Acc:02d}' + "h.grib"
mv.write(FileOUT, percs_tot_global)