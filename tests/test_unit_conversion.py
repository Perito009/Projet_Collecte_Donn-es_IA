import pytest
import pandas as pd
from Transform.unit_conversion import convert_units

def test_convert_units():
    # Sample DataFrame for testing
    df = pd.DataFrame({
        'length_m': [1.0, 2.0, 3.0],
        'weight_kg': [10.0, 20.0, 30.0]
    })
    
    # Unit mapping for conversion
    unit_map = {
        'length_m': 3.28084,  # Convert meters to feet
        'weight_kg': 2.20462   # Convert kilograms to pounds
    }
    
    # Expected DataFrame after conversion
    expected_df = pd.DataFrame({
        'length_m': [3.28084, 6.56168, 9.84252],
        'weight_kg': [22.0462, 44.0924, 66.1386]
    })
    
    # Perform unit conversion
    converted_df = convert_units(df, unit_map)
    
    # Assert that the converted DataFrame matches the expected DataFrame
    pd.testing.assert_frame_equal(converted_df, expected_df)