# rapid-remapping
Ocean model output is usually obtained on the native grid used in the initial generation of the data. In many cases, the first step needed to analyze this output is "remapping" or "regridding" from the native coordinates (such as the Arakawa C-grid in the Nucleus for European Modelling of the Ocean) to a latitude-longitude system. This remapping step is a major performance bottleneck as it involves computationally complex interpolation on every field, at every time, at each level, for each realization. For three-dimensional data at monthly time resolution in an ensemble modeling experiment, such as the [UKESM-ARISE-SAI-1.5](https://doi.org/10.5194/egusphere-2023-980) project, this remapping process may take several weeks using approaches such as Scipy's `interp.griddata` method.

The [xESMF](https://pangeo-xesmf.readthedocs.io/en/latest/) package provides a Python wrapper for an extraordinarily fast Fortran implementation of remapping. `rapid-remapping` additionally leverages multiprocessing to allow for parallel processing of multiple files simultaneously. Using six cores on the Colorado State University ASHA high-performance computing cluster, the entire UKESM-ARISE-SAI-1.5 ocean temperature dataset can be remapped in approximately 15 minutes. A back-of-the-envelope calculation indicates that my previous best method (as in [SAI-ESM](https://github.com/dmhuehol/SAI-ESM) using Scipy) would not complete for at least 25 days--so this is a *very* significant improvement!

# Workflow
Once before first run: obtain a reference grid file (single timestep of any data with desired lat/lon grid) which will be used to provide target grid for all future remapping  
Adjust input variables at start of `remap_ocean_data` (documented in docstring) and run!  

On ASHA, the script `run_remap_ocean_data` can be submitted to the job scheduler.

# Credit
Unless specified otherwise, all code and documentation was written by [Daniel Hueholt](https://www.hueholt.earth/) as a Graduate Research Assistant advised by [Prof. Elizabeth Barnes](https://sites.google.com/view/barnesgroup-csu) and [Prof. James Hurrell](https://sites.google.com/rams.colostate.edu/hurrellgroup/home) at Colorado State University.

This work was supported by the National Science Foundation Graduate Research Fellowship Program.

Code in this project is licensed under the Open Software License 3.0, included with this repository as LICENSE.txt.
