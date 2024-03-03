import pandas as pd
from fuzzywuzzy import process



def _match(value, choices):
    if len(choices) == 0:
        return _, 0
    match_, coeff = process.extractOne(value, choices)
    return match_, coeff




def _merge(df1, df2, column_name, threshold=60):
    
    df2_copy = df2.copy()
    choices = df1[column_name].tolist()

    for index, row in df2_copy.iterrows():
        value = row[column_name]
        match_, coeff = _match(value, choices)

        if coeff >= threshold:
            df2_copy.at[index, column_name] = match_
            choices.remove(match_)

    df_out = pd.merge(df2_copy,df1,how='outer')
    return df_out



def merge(*dfs, column_name):
    """
    Merge multiple DataFrames iteratively using the specified column ID.
    
    Args:
        *dfs (DataFrame): Multiple DataFrames to be merged.
        column_name (str): The column to perform the merge on.
        
    Returns:
        DataFrame: Merged DataFrame.
    """
    if len(dfs) < 2:
        raise ValueError("At least two DataFrames are required for merging.")
    
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = _merge(merged_df, df, column_name)
    
    return merged_df

