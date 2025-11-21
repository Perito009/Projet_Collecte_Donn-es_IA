import pandas as pd

def normalize_dates(df, date_cols, format='%Y-%m-%d'):
    """
    Normalize date columns in the DataFrame to a specified format.

    Parameters:
    - df: DataFrame containing the data.
    - date_cols: List of columns to normalize.
    - format: The desired date format (default is '%Y-%m-%d').

    Returns:
    - DataFrame with normalized date columns.
    """
    for col in date_cols:
        if col in df:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime(format)
    return df