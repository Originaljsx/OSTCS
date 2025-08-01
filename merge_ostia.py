#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
"""
Global OSTIA Merge with Spatial Subsetting
Merge global files then subset spatially - more efficient than clipping first
"""

import xarray as xr
import pandas as pd
import glob
import os
import geopandas as gpd
from datetime import datetime

def merge_global_ostia_with_subset(input_dir, shapefile_path, output_file, buffer_degrees=0.1):
    """
    Merge global OSTIA files and subset spatially in one operation
    """
    
    print(" GLOBAL OSTIA MERGE WITH SPATIAL SUBSETTING")
    print("=" * 60)
    
    # Find global OSTIA files
    file_pattern = os.path.join(input_dir, "*OSTIA*.nc")
    files = sorted(glob.glob(file_pattern))
    
    if not files:
        print(f" No OSTIA files found in {input_dir}")
        return
    
    print(f" Found {len(files)} global OSTIA files")
    print(f"   First: {os.path.basename(files[0])}")
    print(f"   Last:  {os.path.basename(files[-1])}")
    
    # Get spatial bounds from shapefile
    print(f" Reading spatial bounds from: {shapefile_path}")
    gdf = gpd.read_file(shapefile_path)
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    
    # Add buffer
    minx, miny, maxx, maxy = bounds
    bounds_buffered = (
        minx - buffer_degrees,
        miny - buffer_degrees, 
        maxx + buffer_degrees,
        maxy + buffer_degrees
    )
    
    print(f"   Spatial bounds: {bounds}")
    print(f"   With buffer: {bounds_buffered}")
    
    # Estimate size
    if files:
        sample_size = os.path.getsize(files[0]) / (1024**3)
        total_size_gb = sample_size * len(files)
        print(f" Estimated global dataset: {total_size_gb:.1f} GB")
    
    try:
        print(f"\n Opening global multi-file dataset...")
        print("   Using chunked processing - this is memory efficient!")
        
        # Open with chunking - this is key for memory efficiency
        ds_global = xr.open_mfdataset(
            files,
            concat_dim='time',
            combine='nested',
            parallel=True,
            chunks={'time': 30, 'lat': 200, 'lon': 200},  # Conservative chunks
            coords='minimal',
            data_vars='minimal',
            decode_times=True
        )
        
        print(f" Global dataset opened successfully!")
        print(f"   Global shape: {dict(ds_global.dims)}")
        print(f"   Time range: {ds_global.time.min().values} to {ds_global.time.max().values}")
        print(f"   Variables: {list(ds_global.data_vars.keys())}")
        
        # Spatial subsetting - this is where the magic happens
        print(f"\n Spatial subsetting to study area...")
        
        # Handle different coordinate names
        if 'longitude' in ds_global.coords:
            lon_name, lat_name = 'longitude', 'latitude'
        elif 'lon' in ds_global.coords:
            lon_name, lat_name = 'lon', 'lat'
        else:
            print(" Cannot find longitude/latitude coordinates!")
            return
        
        print(f"   Using coordinates: {lat_name}, {lon_name}")
        
        # Subset spatially using .sel() - this is very efficient with dask
        minx_buf, miny_buf, maxx_buf, maxy_buf = bounds_buffered
        
        ds_subset = ds_global.sel(
            {lon_name: slice(minx_buf, maxx_buf),
             lat_name: slice(miny_buf, maxy_buf)}
        )
        
        print(f" Spatial subset complete!")
        print(f"   Subset shape: {dict(ds_subset.dims)}")
        print(f"   Reduction: {ds_global.dims['lat']} → {ds_subset.dims['lat']} lat points")
        print(f"              {ds_global.dims['lon']} → {ds_subset.dims['lon']} lon points")
        
        # Sort by time
        print(f"\n Sorting by time...")
        ds_subset = ds_subset.sortby('time')
        
        # Add metadata
        ds_subset.attrs.update({
            'title': 'OSTIA L4 SST Analysis - Spatially Subsetted',
            'created_from': f"{len(files)} global OSTIA files",
            'spatial_subset': f"lon: {minx_buf:.2f} to {maxx_buf:.2f}, lat: {miny_buf:.2f} to {maxy_buf:.2f}",
            'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_dataset': 'OSTIA L4 GHRSST Global',
            'processing_method': 'global merge + spatial subset',
            'buffer_degrees': buffer_degrees
        })
        
        # Prepare encoding
        print(f"\n Saving subsetted dataset to: {output_file}")
        encoding = {}
        for var in ds_subset.data_vars:
            encoding[var] = {
                'zlib': True,
                'complevel': 1,
                'chunksizes': (30, min(100, ds_subset.dims['lat']), min(100, ds_subset.dims['lon'])),
                'dtype': 'float32'
            }
        
        # Save - this triggers the actual computation
        print("   Computing and writing data (this may take 15-45 minutes)...")
        ds_subset.to_netcdf(output_file, encoding=encoding)
        
        # Results
        file_size_gb = os.path.getsize(output_file) / (1024**3)
        
        print(f" Created: {output_file}")
        print(f" File size: {file_size_gb:.1f} GB")
        print(f" Final dataset:")
        print(f"   Time steps: {ds_subset.time.size}")
        print(f"   Spatial grid: {ds_subset.dims['lat']} × {ds_subset.dims['lon']}")
        print(f"   Time range: {ds_subset.time.min().values} to {ds_subset.time.max().values}")
        print(f"   Variables: {list(ds_subset.data_vars.keys())}")
        
        # Data quality check
        first_var = list(ds_subset.data_vars.keys())[0]
        sample_data = ds_subset[first_var].isel(time=0, lat=0, lon=0).values
        print(f"   Sample {first_var}: {sample_data}")
        
        # Check for time gaps
        if ds_subset.time.size > 1:
            time_diffs = pd.to_datetime(ds_subset.time.values[1:]) - pd.to_datetime(ds_subset.time.values[:-1])
            gaps = time_diffs[time_diffs > pd.Timedelta(days=1)]
            if len(gaps) > 0:
                print(f"    Time gaps: {len(gaps)} missing days")
            else:
                print(f"    Complete daily coverage")
        
        # Cleanup
        ds_subset.close()
        ds_global.close()
        
        print(f"\n Global merge and subset completed successfully!")
        
    except MemoryError as e:
        print(f"\n Memory Error: {e}")
        print(f" Try smaller chunks: chunks={{'time': 10, 'lat': 100, 'lon': 100}}")
        
    except Exception as e:
        print(f"\n Error: {e}")
        print(f"Error type: {type(e).__name__}")

def quick_feasibility_check(input_dir):
    """Quick check to see if this approach is feasible"""
    
    files = sorted(glob.glob(os.path.join(input_dir, "*OSTIA*.nc")))
    if not files:
        print("No OSTIA files found!")
        return False
    
    print(f" Feasibility check with {len(files)} files...")
    
    # Test opening a few files
    test_files = files[:3]
    for f in test_files:
        try:
            with xr.open_dataset(f) as ds:
                print(f"    {os.path.basename(f)}: {dict(ds.dims)}")
        except Exception as e:
            print(f"    {os.path.basename(f)}: {e}")
            return False
    
    # Estimate memory requirements
    sample_size = os.path.getsize(files[0]) / (1024**3)
    total_size = sample_size * len(files)
    
    print(f" Dataset size: {total_size:.1f} GB")
    print(f" Chunked processing will use ~2-4 GB RAM max")
    
    return total_size < 500  # Reasonable limit

def main():
    # Configuration
    input_dir = "OSTIA_global"  # Your global files directory
    shapefile_path = "Study_Areas/Bound_Box_UPD.shp"
    output_file = "OSTIA_global_merged_subset.nc4"
    
    # Quick feasibility check
    if not quick_feasibility_check(input_dir):
        print(" Dataset too large or files corrupted")
        return
    
    # Run the merge and subset
    merge_global_ostia_with_subset(
        input_dir=input_dir,
        shapefile_path=shapefile_path,
        output_file=output_file,
        buffer_degrees=0.1
    )

if __name__ == "__main__":
    main()

