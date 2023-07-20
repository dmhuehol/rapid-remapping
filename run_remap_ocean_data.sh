#!/bin/bash

#SBATCH --partition=bar_all
#SBATCH --job-name=rapid_remap
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=logfile_rapid_remap.txt

python remap_ocean_data.py