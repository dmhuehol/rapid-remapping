'''  fun_rapid_remap
Contains function to apply Regridder object from xESMF and save remapped data
as a netCDF file; this is separated from remap_ocean_data for multiprocessing.

Written by Daniel Hueholt
Graduate Research Assistant at Colorado State University
'''
import sys

from icecream import ic
import xarray as xr

def rapid_remap(ocn_da, remap_obj):
    ''' Rapid remapping with xesmf '''
    data_remap = remap_obj(ocn_da) # Apply Regridder

    dkey = ocn_da.name
    new_dset = xr.Dataset(
        {dkey: (("time","lev","lat","lon"), data_remap.data)},
        coords={
            "time": ocn_da.time,
            "lev": ocn_da.lev,
            "lat": remap_obj.out_coords['lat'],
            "lon": remap_obj.out_coords['lon']
        }
    )
    new_dset[dkey].attrs = ocn_da.attrs
    str_out = ocn_da.attrs['in_fname'].replace(".nc","_remap.nc")
    out_file = ocn_da.attrs['out_path'] + str_out
    new_dset.to_netcdf(out_file)
    ic(str_out, out_file, new_dset)