import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###################################################################
# CODE DESCRIPTION
# 03_Compute_ClimateSA.py computes modelled rainfall climatology for a specific
# sub-area.
# Code runtime: the code will take up to x hours.

# DESCRIPTION OF INPUT PARAMETERS
# BaseDateS (date, in the format YYYYMMDD): start date to consider.
# BaseDateF (date, in the format YYYYMMDD): final date to consider.
# Acc (integer, in hours): rainfall accumulation period.
# NumSA (integer): number of total considered sub-areas.
# SA_2_Compute (integer): index for the sub-area to consider.
# Perc_list (list of integers): list of percentiles to compute.
# SystemFC (string): forecasting system to consider.
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory containing ERA5.
# DirOUT (string): relative path for the output directory containing the climatology.

# INPUT PARAMETERS
BaseDateS = datetime(2000,1,1,0)
BaseDateF = datetime(2020,12,31,0)
Acc = 12
NumSA = 160
SA_2_Compute = int(sys.argv[1])
Perc_list = np.append(np.arange(1,100), np.array([99.4, 99.5,99.8,99.95]))
SystemFC = sys.argv[2]
GitRepo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_FlashFlood_Thr"
FileIN_Sample_Grib_Global = "Data/Raw/Sample_Grib_Global.grib"
DirIN_RainSA = "Data/Compute/Reanalysis_SA"
DirOUT = "Data/Compute/ClimateSA"
###################################################################


# Reading the global field for the sample grib
sample_grib_global = mv.read(GitRepo + "/" + FileIN_Sample_Grib_Global)
NumGP_g = int(mv.count(mv.values(sample_grib_global)))
NumGP_sa = int(NumGP_g / NumSA)

# Initializing the variable that will contain the indipendent rainfall realizations for the full period, for a specific sub-area
tp_full_period_sa = np.empty((NumGP_sa,0))
      
# Reading the indipendent rainfall realizations for the full period, for a specific sub-area
print("Reading the indipendent rainfall realizations for " + SystemFC + ", for the full climatological period and for the sub-area n." + str(SA_2_Compute) + "/" + str(NumSA))
BaseDate = BaseDateS
while BaseDate <= BaseDateF:

      print(" - Processing the date: ", BaseDate)
      DirIN_temp = GitRepo + "/" + DirIN_RainSA + "/" + SystemFC + "_" + f'{Acc:02d}' + "h" + "/" + BaseDate.strftime("%Y%m%d")
      FileIN_temp = "tp_" + BaseDate.strftime("%Y%m%d") + "_" + f'{SA_2_Compute:03d}' + ".npy"
      tp_SA = np.load(DirIN_temp + "/" + FileIN_temp)
      tp_full_period_sa = np.hstack((tp_full_period_sa, tp_SA))     

      BaseDate = BaseDate + timedelta(days=1)

# Computing the rainfall climatology as percentiles
print("Computing the rainfall climatology as percentiles")
percs_sa = np.percentile(tp_full_period_sa, Perc_list, axis=1).T
      
# Saving the rainfall climatology for the specific sub-area
print("Saving the rainfall climatology")
DirOUT_temp = GitRepo + "/" + DirOUT + "/" + SystemFC + "_" + f'{Acc:02d}' + "h"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
FileOUT_temp = "ClimateSA_" + f'{SA_2_Compute:03d}' + ".npy"
np.save(DirOUT_temp + "/" + FileOUT_temp, percs_sa)