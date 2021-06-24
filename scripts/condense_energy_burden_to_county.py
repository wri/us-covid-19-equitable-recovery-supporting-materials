"""Aggregate or condense tract-level energy burden into county-level data.
The output table stores the values of the minimum and maximum tract-level
  energy burden within each county.

Usage: python <script> <input_csv> <output_csv>

"""
import pandas as pd
from sys import argv

df = pd.read_csv(argv[1], encoding='latin-1', dtype=str)
df['energy_burden_percent_income'] = df['energy_burden_percent_income'].astype(int)

gb = df.groupby(['state_code', 'county_code'])
out_df = pd.DataFrame()
out_df['max_burden'] = gb['energy_burden_percent_income'].max()
out_df['min_burden'] = gb['energy_burden_percent_income'].min()

out_df.reset_index().to_csv(argv[2], index=False)

