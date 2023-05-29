# Open data plan
Assuming the full output from model output that this metadata tool has post-processed is in the TB range, and is over
a range of variables and a much longer time range than the three hours in the sample data, the following desricbes the 
principles and steps/tools required to make the post-processed data an open dataset.

## Principles
To make output from this code/tool a publically accesible and fully open data publication, we need to ensure the following:
- **Findability**: the dataset should be easy to find, identify and access. There should be a peristent identifier like a 
  DOI associated with version of the dataset, which directs to an entry for the dataset in a public repository. The entry 
  within the repository should have rich and descriptive metadata associated with it (i.e. tags, descripitions, etc) so that 
  a search of the repository for relevant keywords should allow the dataset to be found.
- **Accessibility**: the data needs to be available through an open license, such that there are no restrictions on obtaining 
  and using the data. Futhermore, the data needs to be obtainable through a reasonably standard protocol (eg. HTTP, FTP) 
  such that common and widespread tools can be used to obtain the data.
- **Interoperability**: the data needs to be in a common, non-propeitary format, and needs the data and metadata associated 
  with it to meet common conventions for the field in which it exists. Futhermore, where possible, the metadata should reference 
  the records for the code, input data, projects, funding bodies etc. involved in the making of the dataset.
- **Reusability**: there should be enough information on how the data was generated for a user to trust the quality of the
  dataset, there should be enough metadata and information for a user to know how to use the data for their own purposes, and 
  the data should be available under a licence that allows for its reuse.
  
## Tools/platforms required
With the above as guiding principles, making the full post-processed data an opendata set requires the following:
- **A data repository host**: for a dataset in the TB range, the options here are relatively limited. The most realistic option is to have 
  the data hosted in a project on NCI, which will require the data being part of a project with existing disk space or funding 
  for a project with suitable disk space, but aids in accessibility and interoperability for other Australian users with NCI 
  access and can provide access for non-NCI users through Thredds. CSIRO appears to have its own data servers for open data, which 
  are also an option, but do somewhat reduce the ease with which data can be reused by other Australian researchers.
- **_At least_ one entry in a metadata repostiory/data catalogue**: If NCI is used as the data repository, an entry in the [NCI Data 
  catalogue/geonetwork](https://geonetwork.nci.org.au/) with a DOI and suitable metadata entries is the *bare minimum*. As long as a single 
  DOI is used, having entries in many data catalogues is fine as long as they are relevant to the dataset, and contain an appropriate amount 
  of metadata to aid in findability and reusability. For example, entries in the [Australian Research Data Commons](https://researchdata.edu.au/) 
  and CSIRO's own [Data Access Portal](https://data.csiro.au/) are highly advisable (and likely required in regards to the CSIRO Data Access Portal).
  The metadata in these entries should contain references to the data catalogue entry for the ACCESS-CM2 data prepared for the CMIP6 experiment SSP370, 
  references to software for this post-processing code, the CCAM model and the ACCESS-CM2 model, to the Australian Climate Hazards project and to 
  the specifications for the CMIP6 SSP370 experiment (hopefully, all of these have their own entries in repositories with DOIs and following FAIR principles,
  or where at least metadata for each of these can be found).
- **Adherence to common conventions**: In this case, at least [CF compliance](http://cfconventions.org/) for the post-processed netCDF files 
  and, depending on the data catalogue, metadata meeting at least one of [ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) 
  compliance, ISO19115-2 compliance, or compliance with the data catlogue's own metadata specifications. The post-processing code here should 
  ensure the netCDF files are CF-compliant.
