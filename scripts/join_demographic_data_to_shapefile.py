"""Merge tabular data into a county-level shapefile.

Usage: python <script> <demographic_csv> <energy_burden_csv> <input_shapefile> <output_shapefile>

"""
import csv
from sys import argv
import fiona

# make dictionaries of { (state, county): value, ... }
non_white = {(x['state_code'], x['county_code']): x['non_white_ratio'] for x in csv.DictReader(open(argv[1]))}
energy_burden = {(x['state_code'], x['county_code']): x['max_burden'] for x in csv.DictReader(open(argv[2]))}


with fiona.open(argv[3]) as shpin:
	schema = shpin.schema
	crs = shpin.crs
	driver = shpin.driver
	# update the schema to include new fields
	# ratio of non-white residents (in range 0-1)
	schema['properties']['nonwhite'] = 'float:12.5'
	# percentage (as %) of income spent on energy
	schema['properties']['burden'] = 'int:3'
	# class / category for demographics
	schema['properties']['cls_demo'] = 'str:1'
	# class / category for energy burden
	schema['properties']['cls_burd'] = 'str:1'
	# class / category for demographics & energy burden pair
	schema['properties']['cls_bivar'] = 'str:2'

	# open new shapefile for writing
	with fiona.open(argv[4], 'w', schema=schema, crs=crs, driver=driver) as shpout:
		for s in shpin:
			# get the state and county FIPS codes
			gid = s['properties']['GEOID']
			state_id = gid[:2]
			county_id = gid[2:5]
			# look up the energy or demographic data for that (state, county) pair
			# if not found, use value (-1), which is an impossible value for either metric
			burden = int(energy_burden.get((state_id, county_id), -1))
			demo = float(non_white.get((state_id, county_id), -1))
			# set demographic and burden values for this county
			s['properties']['nonwhite'] = demo
			s['properties']['burden'] = burden

			# assign class for the demographic - use 'X' if data not available
			if demo >= 0.25:
				s['properties']['cls_demo'] = 'C'
			elif demo >= 0.10:
				s['properties']['cls_demo'] = 'B'
			elif demo >= 0:
				s['properties']['cls_demo'] = 'A'
			else:
				s['properties']['cls_demo'] = 'X'

			# assign class for the burden - use '0' if data not available
			if burden >= 15:
				s['properties']['cls_burd'] = '3'
			elif burden >= 7:
				s['properties']['cls_burd'] = '2'
			elif burden >= 0:
				s['properties']['cls_burd'] = '1'
			else:
				s['properties']['cls_burd'] = '0'

			# concatenate the two classes to produce one of 9 possible valid values
			# there are 16 possible values (if including 'X' and '0'), but only 9 that are valid / complete
			s['properties']['cls_bivar'] = s['properties']['cls_demo'] + s['properties']['cls_burd']

			# save this modified version of the county feature
			shpout.write(s)

