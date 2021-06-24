# Supporting Material for WRI Publication ""
[Link to publication]()

**This publication is under review. This repository and the data should not be shared externally at this time.**

# Purpose

Figure X of the WRI Issue Brief "" is a map that displays both household energy burden and a form of racial demographics at a county level for the US, including the District of Columbia but not including US territories.
This repository holds the processing workflow to recreate that map (up to producing a shapefile with the categories for the [bivariate choropleth](https://www.joshuastevens.net/cartography/make-a-bivariate-choropleth-map/)).


# Usage

This repo can do the full processing in one step if you have the python libraries installed and ready (see `requirements.txt`).
Otherwise, you will want to work within a virtual environment.

```
# any common python version should work... only very basic functionality is used
# python >= 3.7 is recommended
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

The full pipeline can be ran with `make` -- see the `Makefile` for the workflow.

```
make all
```

The output county-level shapefile is located at `derived/county_2018_all_fields.shp`.


# Data Sources
All input files and data sources are works of the United States Government in the public domain.

## census tract-level energy burden
`manual_input/tract_energy_burden.csv` is compiled from the [US DOE LEAD tool](https://www.energy.gov/eere/slsc/maps/lead-tool), which does not seem to offer a full download at a URL.
For this reason, we manually downloaded tract data for each state (plus DC) using the "Area Median Income (AMI)" income model.
These were concatenated into one table using Microsoft Excel and saved as a CSV.

Subsequently, these tract-level data are aggregated into county-level data based on the maximum tract-level energy burden within each county.


## census county-level demographics
`raw/cc-est2018-alldata.csv` comes from the [Census Bureau's Population Estimates Program](https://www.census.gov/programs-surveys/popest.html).
We use data for year 2018 which matches the DOE LEAD use of American Community Survey 2018 microdata samples.

Further processing of the demographic data is performed to produce a value for the proportion of 'non-white' residents within each county.


## geography and geospatial geometries
`raw/tlgdb_2018_a_us_substategeo.gbd` comes from the Census Bureau's TIGER/Line data.
Both county and state geographies are extracted and used in the map.


# License
The software in this repository (`Makefile` and `scripts/*`) are licensed under the MIT license. See `LICENSE` for full license text.
The output file `derived/county_2018_all_fields.shp` and associated derived files are licensed under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) license.

