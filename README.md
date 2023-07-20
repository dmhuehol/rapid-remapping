# rapid-remapping
Ocean model data is usually obtained on the native grid used in the initial generation of the data. The first step when working with ocean model output is often "remapping" the data from this native grid (such as the Arakawa C-grid in the Nucleus for European Modelling of the Ocean) to the latitude-longitude coordinates needed for analysis. (Remapping is often referred to as ``regridding" or ``interpolation".) This remapping step is often one of the principle bottlenecks in a workflow as it involves computationally complex interpolation on every field, at every timestep, at each level, for each realization. For three-dimensional data at monthly timesteps in an ensemble modeling experiment, such as the UKESM-ARISE-1.5 project, this remapping process may take days to weeks using approaches such as Scipy's `interp.griddata` method.

The [xESMF](https://pangeo-xesmf.readthedocs.io/en/latest/) package provides a Python wrapper for an extraordinarily fast Fortran implementation of remapping. **On a 2020 MacBook Pro, this implementation allows for the remapping of a single relization of 15 years of global data at monthly timestep with 75 vertical levels in approximately 90 seconds.** The `rapid-remapping` package additionally uses multiprocessing to allow for parallel processing of multiple files simultaneously. Using six cores on the Colorado State University ASHA high-performance computing cluster, the entire UKESM-ARISE-1.5 dataset can be remapped in approximately 15 minutes.

# Workflow
Adjust input variables at start of `remap_ocean_data` and run!  
 * Input variables are documented in the docstring for `remap_ocean_data`
 * You will need a reference grid file (single timestep with desired lat/lon grid)  

On ASHA, the script `run_remap_ocean_data` can be submitted to the job scheduler.

# Credit
Unless specified otherwise, all code and documentation was written by [Daniel Hueholt](https://www.hueholt.earth/) as a Graduate Research Assistant advised by [Prof. Elizabeth Barnes](https://sites.google.com/view/barnesgroup-csu) and [Prof. James Hurrell](https://sites.google.com/rams.colostate.edu/hurrellgroup/home) at Colorado State University.

This work was supported by the National Science Foundation Graduate Research Fellowship Program.

Code in this project is licensed under the Open Software License 3.0, included with this repository as LICENSE.txt.
