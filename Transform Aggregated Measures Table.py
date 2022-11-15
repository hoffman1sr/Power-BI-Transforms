import pandas as pd
df_AggMeasures = pd.read_csv(r'C:\Users\SHoffman\Downloads\Aggregated Measures Table.csv')

# Get scenarios and create the new columns by getting the scenarios from measure column
scenarios = df_AggMeasures['Scenario'].drop_duplicates().values
newcolumns = ['Year']
newcolumns.extend( df_AggMeasures['measure'].drop_duplicates().values.tolist() )
newcolumns.append('Scenario')

# This will tranpose over scenario at a time. 
def transposer(scenario, df):  
    temp = df.loc[ df['Scenario']== scenario ].T.reset_index() # Rotate the data
    temp['Scenario'] = scenario # Create a new column with the current scenario name

# Get the the new transposed column names, and the desired column names. Add to dictionary and rename columns.
    columns_dict = {}
    i=0
    for entry in temp.columns:
        columns_dict[entry] = newcolumns[i]
        i+=1

    temp = temp.rename(columns=columns_dict)
    temp = temp.iloc[2:][:]
    return temp

# Transpose the chunks for each scenario and concat it all together
final_df = pd.DataFrame(columns=newcolumns)
for scenario in scenarios:
    temp = transposer(scenario, df_AggMeasures)
    final_df = pd.concat([final_df, temp])