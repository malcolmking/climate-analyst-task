# CCAM Metadata Tool
CCAM Metadata Tool is a small python script/module which adds metadata to a CCAM model output dataset 
to improve the readability and useability of the data, and to attempt to make the dataset [CF-compliant](http://cfconventions.org/). 
This initial version (v0.1) is only functional for a single data variable (tas - near surface air 
temperature), but is designed to be more generally applicable in future.

This code has been tested in Python 3.9, and compatibility is only ensured for Python 3.9 and above.

# Module dependencies
This code requires the following python modules:
- [numpy](https://numpy.org/)
- [xarray](https://xarray.dev/)
- A netcdf I/O module compatible with xarray ([scipy](https://scipy.org/), [netcdf4-python](https://unidata.github.io/netcdf4-python/), [h5netcdf](https://github.com/h5netcdf/h5netcdf))

# How to use
## From command line
`python CCAM_metadata_tool.py input_file output_file`

`input_file`: The file or file-path to the raw data file to which the metadata will be added.

`output_file`(optional): file or file-path where the data with additional metadata will be saved. 
If not specified, an output file will be made in the working directory with a self-generated file name.
## As a module (within a python script)
```python
import CCAM_metadata_tool as cmt

cmt.apply_metadata(input_file,output_file,global_metadata)
```

`input_file`: The file or file-path to the raw data file to which the metadata will be added.

`output_file`(optional): file or file-path where the data with additional metadata will be saved. 
If not specified, an output file will be made in the working directory with a self-generated file name.

`global_metadata`(optional): a dictionary of metadata fields (as keys) and metadata (as entries) which will
supersede the default global_metadata defined within the script. *Note: The default global metadata is known
to be CF-compliant, this will likely not be the case if you specify your own global metadata.*
## Testing
Using the `tas_ccam_2015_raw.nc` file as an input file, as in

`python CCAM_metadata_tool.py tas_ccam_20150101_raw.nc`

should generate the `tas_AUS-10i_CCAM_ACCESS-CM2_20150101T01-20150101T03.nc` file. This file was checked for CF-1.8 
compliance using the [IOOS Compliance Checker](https://compliance.ioos.us/index.html).

# Known issues
- Only works for tas as an input data variable
- Assumes (unless used as a module and global metadata is specified) all input data has the same domain and forcing as the test input file

# Licence
This code is licenced for use under a [GNU General Public License v3.0](https://github.com/malcolmking/climate-analyst-task/blob/main/LICENSE).
It is generally free for use and modification, given that any derivative works are available under the same 
licence (for more exact information, check the licence).

# Contribute
Anyone is welcome to contribute to this project! Leave comments/fixes/suggestions in the issues tab above.

# Open data for outputs
A short statement about principles and steps/tools required for open publication of output data from this tool can be [found here](https://github.com/malcolmking/climate-analyst-task/blob/main/OPEN_DATA_PLAN.md).

# More information
- [CCAM model](https://confluence.csiro.au/display/CCAM/CCAM)
