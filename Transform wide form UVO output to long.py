# Transform wide form UVO output to long form for Power BI
import pandas as pd
csv_location = r'C:\Users\SHoffman\Downloads\Detailed Measures Table.csv'

# Load CSV get years and KPIs
wide_df = pd.read_csv(csv_location)
years = list( wide_df.columns[6:] )
kpis = list( wide_df['measure'].drop_duplicates().values )
wide_df = wide_df.set_index(['project', 'name', 'Scenario']) #Set project number, Name, & Scenario as the index so we can keep them

# Melt along each access to convert wide form to short form. Iterate for each KPI. Concatenate it all back together at the end. 
melted_dfs = []
for item in kpis:
    temp_df = wide_df.loc[ wide_df['measure'] == item ]
    temp_df = pd.melt( temp_df, value_vars = years, var_name = 'Year', value_name = item, ignore_index=False)
    melted_dfs.append(temp_df)

# Concat the melted DFs all back together and reset indexes so PowerBI will see them as columns.
USETHIS_LongDetailedMeasuresDF = pd.concat(melted_dfs, axis=1).sort_index()
USETHIS_LongDetailedMeasuresDF = USETHIS_LongDetailedMeasuresDF.loc[:,~USETHIS_LongDetailedMeasuresDF.columns.duplicated()].copy() #Drop duplicate year coumns
USETHIS_LongDetailedMeasuresDF = USETHIS_LongDetailedMeasuresDF.reset_index()