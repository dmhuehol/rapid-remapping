'''  remap_ocean_data
Parallelized remapping of ocean model output from ocean grid into lat/lon
with data saved as netCDF files. This code should work with any model given a 
grid file (implemented: Nucleus for European Modelling of the Ocean [NEMO]).

Input variables are located at the start of the file and documented here.
data_path: Directory with data to be remapped (include trailing slash)
out_path: Directory to save remapped data (include trailing slash)
data_var: Manually provide variable name in input files, examples below
    'thetao': 3D ocean temperature (CMIP6 format)
    'tos': sea surface temperature (CMIP6 format)
    'TEMP': ocean temperature (CESM unprocessed)
nproc: Spawn nproc+1 number of parallel processes. 
    Theoretical best efficiency is one fewer than system thread count, (e.g.,
    multiprocessing.cpu_count()-1), but memory is often a stricter constraint.
        
NOTE: 'fork' is only supposed to work on Unix-based systems (e.g., Mac, Linux). 
Thus, this code should not run on Windows, although I have not verified this.

Written by Daniel Hueholt
Graduate Research Assistant at Colorado State University
'''
import glob
import multiprocessing as mp
import sys

from icecream import ic
import xarray as xr
import xesmf as xe

import fun_rapid_remap as frr

# Inputs - see docstring for details
# data_path = '/Users/dhueholt/Documents/UKESM_data/monthly_thetao/' #local
data_path = '/scratch/dhueholt/monthly_thetao/' #ASHA
# out_path = '/Users/dhueholt/Documents/UKESM_data/monthly_thetao_remap/' #local
out_path = '/scratch/dhueholt/monthly_thetao_remap/' #ASHA
# gridref_path = '/Users/dhueholt/Documents/UKESM_data/grid_ref/ukesm_arise_latlon.nc' #local
gridref_path = '/scratch/dhueholt/grid_ref/ukesm_arise_latlon.nc' #ASHA
data_var = 'thetao'
nproc = 2

# Open files and instantiate Regridder
str_list = sorted(glob.glob(data_path + "*.nc"))
data_list = list()
for fname in str_list:
    in_dset = xr.open_dataset(fname) # Do NOT use open_mfdataset--times may not match
    in_da = in_dset[data_var]
    in_da.attrs['in_fname'] = fname.replace(data_path, "") # Track individual files
    in_da.attrs['out_path'] = out_path
    data_list.append(in_da) # Place all in single list
grid_ref = xr.open_dataset(gridref_path)
remap = xe.Regridder(data_list[0], grid_ref, "bilinear") # Regridder reused for all

# Remap files in parallel
for da_count, da in enumerate(data_list):
    len_dat = len(data_list)
    if __name__== '__main__': # If statement required by multiprocessing
        mp.set_start_method('fork', force=True)
        shard = mp.Process( # Each parallel process regrids and saves a file
            target=frr.rapid_remap, args=(da, remap))
        if da_count % nproc == 0 and da_count != 0: # Every nproc number of files
            shard.start()
            shard.join() # Complete nproc+1 processes before starting more
            shard.close() # Free up resources to lower load on machine
        else:
            shard.start()
        files_remaining = len_dat - da_count - 1
        numleft = ic(files_remaining) # Cheap "progress bar"
