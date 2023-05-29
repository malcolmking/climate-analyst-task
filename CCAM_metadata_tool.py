"""
CCAM_metadata_tool
-------------------
v0.1 (28-05-2023)
-------------------

This python script provides a tool to apply CF-compliant metadata to raw
CCAM model output, as provided in the format of the sample raw data file in
this directory (tas_ccam_20150101_raw.nc).

Metadata outside of the CF conventions is attempted to match the CMIP6 and/or
CORDEX metadata conventions.

NetCDF and metadata handling is performed by xarray, and thus xarray and its
dependencies are required modules for this script.
"""
import xarray as xr
from datetime import datetime
import numpy as np

"""
Default metadata dictionaries
"""
# The following maps coordinates to dictionaries containing their metadata.
coord_metadata={'lon':{'units':'degrees_east',\
                       'standard_name':'longitude',\
                       'long_name':'longitude',\
                       'axis':'X'},\
                'lat':{'units':'degrees_north',\
                       'standard_name':'latitude',\
                       'long_name':'latitude',\
                       'axis':'Y'},\
                'time':{'standard_name':'time',\
                        'long_name':'time',\
                        'axis':'T'}}

# The following maps data variables to dictionaries containing their metadata.
# At the moment, only works for tas (near-surface temperature), easily extended in future
# Not certain if tas output from CCAM is point-like or grid-cell average; if grid cell average,
# need to add 'cell_method':'area: mean' to dictionary.
datavar_metadata={'tas':{'units':'K',\
                         'standard_name':'air_temperature',\
                         'long_name':'near-surface air temperature'}}

# Dictionary containing default global metadata for the CCAM output described.
global_metadata={'title':'CSIRO CCAM output prepared for Australian Climate Hazards project',\
                 'institution':'Commonwealth Scientific and Industrial Research Organisation (CSIRO)',\
                 'source':'CCAM',\
                 'version':'r5262M',\
                 'driving_model':'ACCESS-CM2',\
                 'driving_insitutuion':'CSIRO-ARCCSS',\
                 'driving_experiment_name':'SSP370',\
                 'contact':'ccam@csiro.au',\
                 'domain':'AUS-10i',\
                 'nominal_resolution':'12km',\
                 'frequency':'1hr',\
                 'Conventions':'CF-1.8'}
"""
Utility functions
"""

def update_coord_metadata(dataset):
    """Looks up coordinates in the metadata dictionary, and applies the corresponding metadata."""
    for coord in dataset.coords:
        if coord not in coord_metadata:
            raise Exception('Co-ordinate not recognised. Coordinates must be lat, lon or time.')
        dataset[coord].attrs.update(coord_metadata[coord])
    return dataset

def update_datavar_metadata(dataset):
    """Looks up datavar in the metadata dictionary, and applies corresponding metadata."""
    for datavar in dataset.data_vars:
        if datavar not in datavar_metadata:
            raise Exception('Data variable not recognised. Currently supported: tas.')
        dataset[datavar].attrs.update(datavar_metadata[datavar])
        if 'fill_value' in dataset[datavar].attrs:
            dataset[datavar].attrs['_FillValue']=dataset[datavar].attrs['fill_value']
            dataset[datavar].attrs['missing_value']=dataset[datavar].attrs['fill_value']
            del(dataset[datavar].attrs['fill_value'])
    return dataset

def update_global_metadata(dataset,global_metadata=global_metadata):
    """Applies global metadata to the dataset.
    
    Can be provided with a dictionary that replaces the default metadata, but this does not
    ensure compliance of the output dataset."""
    # Ensure that history field is updated with current timestamp
    current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%Sz')
    if 'history' in dataset.attrs:
        history=current_time+" ; metadata added by CCAM_metadata_tool.py \n"+dataset.history
    else:
        history=current_time+" ; metadata added by CCAM_metadata_tool.py"
    global_metadata['history']=history
    dataset.attrs.update(global_metadata)
    return dataset
    
def update_metadata(dataset,global_metadata=global_metadata):
    """Applies coordinate, data variable and global metadata to a dataset.
    
    Global metadata can be passed to this as a dictionary, but may result in output
    not matching data conventions."""
    update_coord_metadata(dataset)
    update_datavar_metadata(dataset)
    update_global_metadata(dataset,global_metadata)
    return dataset

def output_file_name(dataset):
    """Attempts to make a sensible output file name, based on data variables and
    global attributes."""
    start_str=np.datetime_as_string(dataset['time'].data[0],unit='h').replace('-','')
    end_str=np.datetime_as_string(dataset['time'].data[-1],unit='h').replace('-','')
    
    if len(dataset.data_vars)==1:
        file_prefix=list(dataset.data_vars.keys())[0]
    else:
        file_prefix='data'
    
    # The below could be cleaned up in future.
    if ('domain' in dataset.attrs) and ('source' in dataset.attrs) and ('driving_model' in dataset.attrs):
        output_file=file_prefix+'_'+dataset.domain+'_'+dataset.source+'_'+dataset.driving_model+'_'+start_str+'-'+end_str+'.nc'
    elif ('domain' in dataset.attrs) and ('source' in dataset.attrs):
        output_file=file_prefix+'_'+dataset.domain+'_'+dataset.source+'_'+start_str+'-'+end_str+'.nc'
    elif ('source' in dataset.attrs) and ('driving_model' in dataset.attrs):
        output_file=file_prefix+'_'+dataset.source+'_'+dataset.driving_model+'_'+start_str+'-'+end_str+'.nc'
    elif ('source' in dataset.attrs):
        output_file=file_prefix+'_'+dataset.source+'_'+start_str+'-'+end_str+'.nc'
    else:
        output_file=file_prefix+'_'+start_str+'-'+end_str+'.nc'
    
    return output_file
    
    
def apply_metadata(input_file,output_file=None,global_metadata=global_metadata):
    """Opens an input file, applies metadata and saves it.
    
    Returns the path of the output file (by default will save it in the working directory)."""
    
    dataset=xr.open_dataset(input_file)
    update_metadata(dataset,global_metadata)
    
    # dtype for time changed to double and _FillValue for coords removed to meet CF conventions.
    encoding={"lon":{'zlib':False,'_FillValue': None},\
              "lat":{'zlib':False,'_FillValue': None},\
              "time":{'zlib':False,'_FillValue':None,'dtype':'double'}}
    for datavar in dataset.data_vars:
        encoding[datavar]={'zlib':True}
        
    if output_file is None:
        output_file=output_file_name(dataset)
        
    dataset.to_netcdf(output_file,encoding=encoding,unlimited_dims='time')
    return 'saved at '+output_file

"""
The following will run if CCAM_metadata_tool.py is run as a script.

Will take an argument file path, and output a file.
"""

if __name__=="__main__":

    # If running as a script, the following will take the first argument after
    # the script name as the input filepath, and the second as the ouput if it
    # is provided.
    import sys
    arguments=sys.argv
    if len(arguments)>=3:
        input_file=arguments[1]
        output_file=arguments[2]
    elif len(arguments)==2:
        input_file=arguments[1]
        output_file=None
    else:
        raise Exception('please specify an input file.')
    
    output=apply_metadata(input_file,output_file)
    print(output)