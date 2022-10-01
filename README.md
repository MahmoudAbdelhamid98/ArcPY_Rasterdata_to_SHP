# ArcPY_Rasterdata_to_SHP
Taking multiple data from Raster data to shapefiles of a sewer network to calculate the infiltration using ArcPY packages

## This code is in intended to solve the following problem:

It is required to estimate the amount of groundwater infiltration to the
sewage trunks provided in the data set as well as the ground levels upstream
and downstream each trunk sewer. The Egyptian code of practice recommends
the following equation for estimating groundwater infiltration to sewage pipes:
Q=∝*d*h^(2/3)
Where Qinf is the leakage discharge (m3/hr/km length), ∝ is constant = 1, d is
pipe diameter (m) and h is the average depth of pipe below ground water (m),
the data given to test your tool is:
- Trunks shapefile containing the sewage trunks
- survey.csv comma delimited spreadsheet containing the ground
survey
- boreholes.csv spreadsheet containing the borehole results

## The main concept is using ArcPY packages to pickup data from rasters to shapefiles
