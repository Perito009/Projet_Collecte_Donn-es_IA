def enrich_df(df, additional_data, on=None, new_columns=None):
    """
    Enriches the DataFrame with additional data.
    
    Parameters:
    - df: The original DataFrame to enrich.
    - additional_data: A DataFrame containing additional data to merge.
    - on: Column name(s) to join on. If None, uses index.
    - new_columns: A list of new columns to compute based on existing data.
    
    Returns:
    - A DataFrame enriched with additional data.
    """
    if on:
        df = df.merge(additional_data, on=on, how='left')
    else:
        df = df.join(additional_data)

    if new_columns:
        for col in new_columns:
            df[col] = df.apply(lambda row: compute_new_column(row), axis=1)

    return df

def compute_new_column(row):
    # Placeholder for logic to compute new column values based on existing data
    return row['existing_column'] * 2  # Example computation, modify as needed