#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
import sys
import xarray as xr

def inspect_nc(path):
    # open the file
    ds = xr.open_dataset(path)
    # print a summary of dims & variables
    print(ds)

    # for each data variable, report shape, dtype, and how many missing values
    for name, da in ds.data_vars.items():
        n_missing = int(da.isnull().sum().values)
        total = da.size
        print(f"{name}: shape={da.shape}, dtype={da.dtype}, missing={n_missing}/{total}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.nc>")
        sys.exit(1)
    inspect_nc(sys.argv[1])



