"""Expand or split a geography code (FIPS) into state, country, and tract values.

Usage: python <script> <input_csv> <output_csv>

"""
import pandas as pd
from sys import argv

df = pd.read_csv(argv[1], encoding='latin-1', dtype=str)
# ensure the code has a leading zero if needed (state FIPS 01-09)
# this is partially a fix to the input data being pulled from 51 files
# and Excel messing with things it thinks are numbers (but are actually strings of numeric digits)
fips_code = df['geography_id'].apply(lambda x: x.zfill(11))
# separate into state, county, tract components (SSCCCTTTTTT) lengths 2-3-6
df['state_code'] = fips_code.str.slice(0, 2)
df['county_code'] = fips_code.str.slice(2, 5)
df['tract_code'] = fips_code.str.slice(5, 11)

df.to_csv(argv[2], index=False)

