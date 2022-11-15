#This is currently set up to examine the difference between a prioritized plan and an optimized plan
import pandas as pd

# Set scenario names in CSV
benchmark = 'Benchmark'
optimized = 'Optimized Plan'
input_csv = 'C:/Users/SHoffman/Downloads/Projects Selection Table.csv'

# Read in projects selection, filter out no proactive spend. 
selection_table = pd.read_csv(input_csv)
selection_table = selection_table[ selection_table['Scenario'] != 'No Proactive Spend' ].reset_index(drop=True)
selection_df = pd.DataFrame(columns=['Name', 'Scenario', 'Selected', 'Start year']) # Create empty dataframe with 

# Gather if project is selected in both scenarios, gather the selection year and add it to the new df
for index, row in selection_table.iterrows():
    years = row[2:]
    if 1 in years.values:
        selected = True
        year = row.index[ 2+list(years.values).index(1) ] # Find where in the row is the 1 marked out. Then feed that back into the row index to determine the year. 
    else:
        selected = False
        year = 0
    newrow = pd.Series({'Name': row[0], 'Scenario': row[1], 'Selected': selected, 'Start year': year})
    selection_df = pd.concat([selection_df, newrow.to_frame().T], ignore_index=True)
    
# Make the benchmark only table and optimized only table
bench_df = selection_df[ selection_df['Scenario'] == benchmark ].drop(['Scenario'], axis=1)
optimized_df = selection_df[ selection_df['Scenario'] == optimized ].drop(['Scenario'], axis=1)

# Rename the columns to make it easier to read for the end table
bench_df = bench_df.rename(columns= {'Selected': 'Selected in Prioritization', 'Start year': 'Prioritization Start' })
optimized_df = optimized_df.rename(columns= {'Selected': 'Selected in Optimization', 'Start year': 'Optimization Start'})

# Merge the benchmark and optimized table back together with an inner merge. Filter to find differences.
both_df = bench_df.merge(optimized_df, on='Name', how='inner')
both_df = both_df.loc[ both_df['Optimization Start'] != both_df['Prioritization Start'] ]
cols = ['Name', 'Selected in Prioritization', 'Selected in Optimization', 'Prioritization Start', 'Optimization Start']
both_df = both_df[ cols ]