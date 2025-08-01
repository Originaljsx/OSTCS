<!-- Header block for project -->
<hr>

<div align="center">

<h1 align="center">Ocean Spatiotemporal Clustering System (OSTCS)</h1>

</div>

<pre align="center">A modular pipeline for geospatial remote sensing data analysis using functional data clustering techniques for oceanographic time series</pre>

<!-- Header block for project -->

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/) [![R](https://img.shields.io/badge/R-4.0+-red.svg)](https://www.r-project.org/) [![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/) [![SLIM](https://img.shields.io/badge/Best%20Practices%20from-SLIM-blue)](https://nasa-ammos.github.io/slim/)

The Ocean Spatiotemporal Clustering System (OSTCS) is a comprehensive geospatial remote sensing pipeline that integrates multi-mission NASA satellite data for oceanographic analysis using time series clustering techniques. The system implements functional data clustering via hypothesis testing k-means (Zambom et al., 2019) adapted for remote sensing applications, processing decade long satellite datasets (2015-2025) to identify temporal patterns independent of spatial location before mapping results geographically.

Developed at NASA JPL, OSTCS supports Earth science missions including SMAP (sea surface salinity), AQUA/MODIS (chlorophyll-a), and OSTIA (sea surface temperature) for operational oceanography research across four major coastal regions: Gulf of Mexico, Caribbean, California Current, and Pacific Northwest.

## Features

### Data Processing & Integration
* **Multi-Mission Satellite Data**: Processing of NASA EarthData (SMAP, AQUA/MODIS), AVISO+ (SWOT), and OSTIA datasets
* **Multi-Resolution Harmonization**: Standardizes data to common 0.10° spatial grid using coarsening and bilinear interpolation
* **Temporal Gap Filling**: Integrates OISSS and SMAP data to create complete time series
* **Regional Clipping**: Automated spatial subsetting using shapefiles for study regions
* **Quality Control**: Comprehensive data validation and diagnostic plotting

### Advanced Clustering Methods
* **Functional Data Clustering**: Implementation of hypothesis testing k-means (Zambom et al., 2019) with ANOVA and t-test statistics
* **Location-Blind Analysis**: Extracts temporal patterns independent of geographic coordinates
* **Statistical Distance Metrics**: Conditional logic using T-statistics (parallelism) and W-statistics (mean differences)
* **GCV-Optimized Smoothing**: Automatic basis function selection (5-(n/3) Fourier functions) with cross-validation

### Analysis & Visualization
* **Hybrid Python-R Architecture**: Python for data processing, R for clustering and statistical analysis
* **Geographic Mapping**: Detailed coastline visualization with state boundaries and bathymetry
* **Cluster Validation**: Elbow plots, silhouette analysis, and medoid identification
* **Time Series Analysis**: Centroid and medoid visualization with seasonal pattern detection
* **Multi-Variable Correlation**: Comparative analysis across SSS, SST, chlorophyll, and sea surface height

## Contents

* [Quick Start](#quick-start)
* [Data Sources](#data-sources)
* [Clustering Methods](#clustering-methods)
* [Analysis Workflows](#analysis-workflows)
* [Visualization](#visualization)
* [License](#license)
* [Support](#support)

## Quick Start

This guide provides a quick way to get started with OSTCS for oceanographic data analysis.

### Requirements

* **Python 3.8+** with packages:
  - `xarray`, `pandas`, `numpy` (data manipulation)
  - `matplotlib`, `cartopy` (visualization)
  - `scikit-learn` (machine learning)
  - `netCDF4`, `requests` (data I/O)
  - `tqdm`, `dask` (parallel processing)
  - `geopandas`, `rioxarray` (geospatial processing)
  
* **R 4.0+** with packages:
  - `fda` (functional data analysis)
  - `terra` (geospatial raster processing)
  - `ggplot2`, `maps`, `mapdata` (visualization)
  - `ncdf4` (NetCDF I/O)
  - `dtw`, `cluster` (time series clustering)
  
* **Credentials & Storage**:
  - NASA EarthData credentials ([register here](https://urs.earthdata.nasa.gov/users/new))
  - AVISO+ credentials for SWOT data ([register here](https://www.aviso.altimetry.fr/en/data/data-access.html))
  - Minimum 100GB available disk space for data processing
  
* **Optional**: Jupyter Notebook for interactive analysis

### Setup Instructions

1. **Set up NASA EarthData credentials**:
   ```bash
   # Create .netrc file in home directory with:
   # machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD
   ```

2. **Configure AVISO+ access** (for SWOT data):
   ```bash
   # Add to .netrc:
   # machine tds-odatis.aviso.altimetry.fr login YOUR_AVISO_USERNAME password YOUR_AVISO_PASSWORD
   ```

3. **Install Python dependencies**:
   ```bash
   pip install xarray pandas numpy matplotlib cartopy scikit-learn netCDF4 requests tqdm dask geopandas rioxarray
   ```

4. **Install R dependencies**:
   ```r
   install.packages(c("fda", "terra", "ggplot2", "maps", "mapdata", "ncdf4", "dtw", "cluster"))
   ```

### Run Instructions

**OSTCS follows a modular Jupyter notebook workflow. Each step corresponds to specific notebooks:**

1. **Preprocessing and Merging**:
   ```bash
   # Download satellite data for your variables:
   jupyter notebook "sss_download.ipynb"                    # SMAP sea surface salinity
   jupyter notebook "SWOT L3 Download.ipynb"               # SWOT sea surface height
   jupyter notebook "OSTIA MO.ipynb"  # OSTIA SST
   
   # Merge individual files into time series:
   jupyter notebook "smap merge.ipynb"                      # Combine SMAP files
   python "merge_ostia.py"                                 # Combine OSTIA files
   jupyter notebook "aquaMODIS merge.ipynb"                # Combine MODIS files 
   jupyter notebook "SWOT L3 Clip and Merge Passes.ipynb"    # Combine SWOT files
   ```

2. **Spatial Processing and Harmonization**:
   ```bash
   # Clip data to study regions using shapefiles:
   jupyter notebook "study 10 gulf nc clip to shp.ipynb"   # Gulf of Mexico
   jupyter notebook "study 10 caribbean nc clip to shp.ipynb"  # Caribbean
   jupyter notebook "study 10 california nc clip to shp.ipynb" # California Current
   
   # Standardize to common 0.10° grid:
   jupyter notebook "Regrid all to .10.ipynb"              # Multi-resolution harmonization
   ```

3. **Functional Data Clustering Analysis on Multidimensional NetCDF Files**:
   ```bash
   # Apply test-based k-means clustering:
   jupyter notebook "gulf sss fkmeans.ipynb"               # Sea surface salinity
   jupyter notebook "gulf sst fkmeans.ipynb"               # Sea surface temperature  
   jupyter notebook "gulf chl fkmeans.ipynb"               # Chlorophyll-a
   jupyter notebook "gulf ssha fkmeans.ipynb"              # Sea surface height anomaly
   ```

### Usage Examples

* **Gulf Salinity Patterns**: Identify Mississippi River influence on salinity distribution using SMAP data (2015-2025)
* **Gulf Sea Surface Temperature Clusters**: Detect Loop Current and Gulf Stream locations
* **Chlorophyll Seasonal Clustering**: Map productivity patterns related to upwelling and nutrient availability
* **Regional Comparative Studies**: Apply consistent methodology across Gulf of Mexico, Caribbean, California, and Pacific Northwest

### Build Instructions (if applicable)

The system is notebook-based and does not require compilation. Simply ensure all dependencies are installed and notebooks can be executed in sequence.

### Test Instructions (if applicable)

1. **Test Data Access**:
   ```bash
   jupyter notebook "inspect_nc.py"  # Verify NetCDF file structure
   ```

2. **Validate Clustering Results**:
   - Check elbow plots for optimal K selection
   - Examine silhouette scores for cluster quality assessment
   - Verify geographic mapping of cluster results

## Data Sources

OSTCS integrates the following satellite datasets from multiple agencies:

### Primary Data Sources:
* **SMAP (Soil Moisture Active Passive)**: Sea surface salinity at 25km resolution
  - JPL CAP SMAP Sea Surface Salinity Products, Ver. 5.0. PO.DAAC, CA, USA. https://doi.org/10.5067/SMP50-3TPCS
  - Daily L3 data from 2015-2025
  
* **OSTIA (Operational Sea Surface Temperature and Sea Ice Analysis)**: Sea surface temperature at 5km resolution
  - UK Met Office OSTIA L4 SST Analysis (GDS2), Ver. 2.0. PO.DAAC, CA, USA. https://doi.org/10.5067/GHOST-4FK02
  - Daily analysis fields
  
* **AQUA/MODIS**: Chlorophyll-a concentrations at 4km resolution
  - NASA Goddard Space Flight Center, Ocean Ecology Laboratory, Ocean Biology Processing Group
  - Moderate-resolution Imaging Spectroradiometer (MODIS) Aqua Chlorophyll Data; NASA OB.DAAC, Greenbelt, MD, USA. doi: 10.5067/AQUA/MODIS/L3M/CHL/2022.0
  - Monthly L3 mapped products
  
* **SWOT (Surface Water and Ocean Topography)**: Sea surface height anomaly at 2km resolution (up to 250m available)
  - AVISO/DUACS SWOT Level-3 KaRIn Low Rate SSH Basic, Ver. 2.0.1. CNES. https://doi.org/10.24400/527896/A01-2023.017
  - Multi-cycle analysis with regional pass compilation

### Gap-Filling Data:
* **OISSS**: Multi-mission L4 Optimally Interpolated Sea Surface Salinity, Ver. 2.0
  - Oleg Melnichenko. 2023. Multi-mission L4 Optimally Interpolated Sea Surface Salinity. Ver. 2.0. PO.DAAC, CA, USA. https://doi.org/10.5067/SMP20-4U7CS
  - Used to fill SMAP gaps during safe mode periods
  - Provides temporal continuity for complete time series

### Data Access Methods:
- **PO.DAAC Data Downloader**: Automated bulk downloads with spatial subsetting via Harmony API
- **OB.DAAC**: Direct download for MODIS chlorophyll products
- **AVISO+ THREDDS Server**: SWOT altimetry data access
- **Hydrocron API**: SWOT river water surface elevation time series extraction

## Clustering Methods

The system implements **functional data clustering via hypothesis testing k-means** based on Zambom et al. (2019):

### Key Features:
- **ANOVA Test Statistics (T)**: Tests for parallelism between time series
- **t-test Statistics (W)**: Tests for differences in means between time series
- **Conditional Logic**: Automatically selects appropriate distance metric based on data characteristics
- **GCV-Optimized Smoothing**: Uses cross-validation to select optimal basis functions (5-40 functions)
- **Location-Blind Analysis**: Identifies temporal patterns independent of geographic location

### Statistical Distance Metrics:
```
Ψ(i,k) = T_stat(i,k) if conditions favor ANOVA testing
         W_stat(i,k) if conditions favor t-testing  
         weighted_average otherwise
```

## Analysis Workflows

### 1. Data Preprocessing Pipeline
- **Automated Downloads**: PO.DAAC data downloader with spatial subsetting (-180°, -50°, 5°, 80°)
- **Temporal Standardization**: Date extraction from filenames and time variable harmonization
- **Gap Filling**: OISSS data integration during SMAP safe mode periods
- **Multi-Resolution Harmonization**: Standardization to 10km target resolution using:
  - OSTIA SST: 5km → 10km (bilinear interpolation)
  - MODIS Chl-a: 4km → 10km (conservative upscaling)
  - SMAP SSS: 25km → 10km (conservative downscaling)
- **Regional Clipping**: Spatial subsetting using study region shapefiles
- **Monthly Averaging**: Temporal aggregation for consistent time series

### 2. Functional Data Conversion
- **Time Series → Fourier Basis Functions**: GCV-optimized smoothing
- **Basis Function Selection**: Automatic selection of optimal number of Fourier functions
- **Individual Curve Smoothing**: Each location treated as separate functional object
- **Quality Control**: Validation of smoothing parameters and functional fits

### 3. Hypothesis Testing K-means Clustering
- **Dual Statistical Testing**:
  - T-statistic: ANOVA test applied to residuals for shape comparison
  - W-statistic: t-test applied to means for level comparison
- **Conditional Assignment Logic**: Adaptive metric selection based on statistical tests
- **Iterative Clustering**: Update centers until convergence or maximum iterations
- **Optimal K Selection**: Within-cluster sum of squares (WCSS) elbow method

### 4. Analysis and Validation
- **Geographic Coherence**: Verification that clusters reflect known oceanographic patterns
- **Cluster Characterization**: Identification of centroids and medoids
- **Physical Interpretation**: Linking clusters to known ocean processes:
  - River outflow effects (Mississippi River influence on Gulf salinity)
  - Ocean current patterns (Loop Current, Gulf Stream detection)
  - Seasonal variability patterns
  - Coastal vs. open ocean dynamics

## Visualization

The system provides comprehensive visualization capabilities:

* **Geographic Cluster Maps**: Coastlines, state boundaries, and river systems
* **Time Series Analysis**: Cluster centroids, medoids, and member curves
* **Statistical Validation**: Elbow plots, silhouette scores, and cluster quality metrics
* **Multi-Panel Comparisons**: Side-by-side analysis of different K values

## License

This software was developed at NASA JPL and is available under an open source license. See [LICENSE](LICENSE) for full terms.

## Support

**Primary Developer**: Jacob Spier (NASA JPL)  
**Technical Contact**: Jorge Vazquez (NASA JPL)



**Key References**:
- Zambom, A.Z., Collazos, J.A.A., and Dias, R. (2019). "Functional data clustering via hypothesis testing k-means." *Computational Statistics*, 34(2), 527-549. DOI: 10.1007/s00180-018-0808-9
- PO.DAAC Cookbook: [https://podaac.github.io/tutorials/](https://podaac.github.io/tutorials/)
- NASA SMAP Mission: [https://smap.jpl.nasa.gov/](https://smap.jpl.nasa.gov/)
- NASA SWOT Mission: [https://swot.jpl.nasa.gov/](https://swot.jpl.nasa.gov/)
- NASA MODIS Mission: [https://modis.gsfc.nasa.gov/](https://modis.gsfc.nasa.gov/)
- Met Office GHRSST OSTIA Product: [https://ghrsst-pp.metoffice.gov.uk/ostia-website/index.html](https://ghrsst-pp.metoffice.gov.uk/ostia-website/index.html)

---

*OSTCS v1.0 - Developed at NASA JPL for operational oceanography research and Earth science mission data analysis. This software supports automated processing workflows for NASA's Earth science data processing infrastructure and enables advanced spatiotemporal pattern detection in satellite datasets.*
