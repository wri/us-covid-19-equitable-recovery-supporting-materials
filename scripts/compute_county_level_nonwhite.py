"""Simplify a census demographics table to calculate ratio of non-white residents in a county.

Usage: python <script> <input_csv> <output_csv>

"""

import pandas as pd
from sys import argv

df = pd.read_csv(argv[1], encoding='latin-1')

# filter to rows with year 2018, all ages; filter to relevant columns
df_subset = df[
    (df.YEAR == 11) &
    (df.AGEGRP == 0)
][['STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'TOT_POP', 'WA_MALE', 'WA_FEMALE']]

# calculate non-white ratio (between 0 and 1)
df_subset['non_white_ratio'] = (df_subset.TOT_POP - df_subset.WA_MALE - df_subset.WA_FEMALE) / df_subset.TOT_POP

# clean the state and county codes, reformat into zero-padded number
df_subset['state_code'] = df_subset.STATE.astype('str').str.zfill(2)
df_subset['county_code'] = df_subset.COUNTY.astype('str').str.zfill(3)

#  save the data to a file, renaming columns
FINAL_COLUMNS = {
	'state_code': 'state_code',
	'county_code': 'county_code',
	'STNAME': 'state_name',
	'CTYNAME': 'city_name',
	'non_white_ratio': 'non_white_ratio'
}

df_subset[FINAL_COLUMNS].rename(columns=FINAL_COLUMNS).to_csv(argv[2], index=False)

