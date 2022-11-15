import pandas as pd
df_AggMeasures = pd.read_csv(r'C:\Users\SHoffman\Downloads\Aggregated Measures Table.csv')

scenarios = df_AggMeasures['Scenario'].drop_duplicates().values
newcolumns = ['Year']
newcolumns.extend( df_AggMeasures['measure'].drop_duplicates().values.tolist() )
newcolumns.append('Scenario')

def transposer(scenario, df):  
    temp = df.loc[ df['Scenario']== scenario ].T.reset_index()
    temp['Scenario'] = scenario

    columns_dict = {}
    i=0
    for entry in temp.columns:
        columns_dict[entry] = newcolumns[i]
        i+=1

    temp = temp.rename(columns=columns_dict)
    temp = temp.iloc[2:][:]
    return temp

final_df = pd.DataFrame(columns=newcolumns)
for scenario in scenarios:
    temp = transposer(scenario, df_AggMeasures)
    final_df = pd.concat([final_df, temp])
    
print(final_df)