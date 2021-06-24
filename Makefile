# build process to get to the final map of US demographics and energy burden
# run `make` or `make all`

## variables ##
raw_dir = raw  # directory for downloads
manual_dir = manual_input  # directory for inputs that are not easy to download
derived_dir = derived  # directory for intermediary and derived data files
script_dir = scripts  # directory holding the processing scripts

census_gdb_url = https://www2.census.gov/geo/tiger/TGRGDB18/tlgdb_2018_a_us_substategeo.gdb.zip
census_gbd = $(raw_dir)/tlgdb_2018_a_us_substategeo.gdb
county_shp_extract = county_2018.shp
state_shp_extract = state_2018.shp

census_est2018_url = https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/asrh/cc-est2018-alldata.csv
census_est2018_csv = cc-est-2018-alldata.csv
census_cleaned_csv = county_non_white_2018.csv

energy_burden_original = tract_energy_burden.csv
energy_burden_expanded = tract_energy_burden_expanded.csv
energy_burden_county_level = county_energy_burden.csv

county_shp_final = county_2018_all_fields.shp


# DEFAULT TARGET - MAKE ALL THE GIS FILES NEEDED FOR THE MAP
all : $(derived_dir)/$(county_shp_final) $(derived_dir)/$(state_shp_extract)

# CENSUS GDB DOWNLOAD (GEOSPATIAL)
$(census_gbd) :
	mkdir -p $(raw_dir)
	wget -O $@.zip $(census_gdb_url)
	unzip $@.zip -d $(raw_dir)
	rm $@.zip


# CENSUS DEMOGRAPHICS TABLE DOWNLOAD
$(raw_dir)/$(census_est2018_csv) :
	mkdir -p $(raw_dir)
	wget -O $@ $(census_est2018_url)


# EXTRACT COUNTY SHAPEFILE FROM GEODATABASE
$(derived_dir)/$(county_shp_extract) : $(census_gbd)
	mkdir -p $(derived_dir)
	ogr2ogr $@ $^ County


# EXTRACT STATE SHAPEFILE FROM GEODATABASE
$(derived_dir)/$(state_shp_extract) : $(census_gbd)
	mkdir -p $(derived_dir)
	ogr2ogr $@ $^ State 


# CONVERT DEMOGRAPHICS TABLE TO SIMPLIFIED FORM
$(derived_dir)/$(census_cleaned_csv) : $(raw_dir)/$(census_est2018_csv)
	mkdir -p $(derived_dir)
	python $(script_dir)/compute_county_level_nonwhite.py $^ $@


# EXPAND ENERGY BURDEN FIPS CODES INTO FULL HIERARCHY
$(derived_dir)/$(energy_burden_expanded) :
	mkdir -p $(derived_dir)
	python $(script_dir)/expand_energy_burden_fips.py $(manual_dir)/$(energy_burden_original) $@


# CALCULATE ENERGY BURDEN VALUES ON A COUNTY BY COUNTY BASIS
$(derived_dir)/$(energy_burden_county_level) : $(derived_dir)/$(energy_burden_expanded)
	mkdir -p $(derived_dir)
	python $(script_dir)/condense_energy_burden_to_county.py $^ $@


# MERGE COUNTY DEMOGRAPHICS AND BURDEN INTO A SHAPEFILE
$(derived_dir)/$(county_shp_final) : $(derived_dir)/$(census_cleaned_csv) $(derived_dir)/$(energy_burden_county_level) $(derived_dir)/$(county_shp_extract) 
	mkdir -p $(derived_dir)
	python $(script_dir)/join_demographic_data_to_shapefile.py \
		$(derived_dir)/$(census_cleaned_csv) \
		$(derived_dir)/$(energy_burden_county_level) \
		$(derived_dir)/$(county_shp_extract) \
		$@

