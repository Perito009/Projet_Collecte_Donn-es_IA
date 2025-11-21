def convert_units(df, unit_map):
    """
    Convert units in the DataFrame based on the provided unit mapping.

    Parameters:
    - df: DataFrame to be processed.
    - unit_map: dict {'col': factor} for converting units (multiplicative factor).

    Returns:
    - DataFrame with converted units.
    """
    for col, factor in unit_map.items():
        if col in df.columns:
            df[col] = df[col].astype('float') * factor
    return df