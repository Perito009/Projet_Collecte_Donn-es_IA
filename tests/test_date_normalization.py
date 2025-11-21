import pandas as pd
import pytest
from Transform.date_normalization import normalize_dates

def test_normalize_dates():
    data = {
        'date_col': ['2023-01-01', '01/02/2023', 'March 3, 2023', None, 'invalid_date']
    }
    df = pd.DataFrame(data)
    expected_dates = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-03-03', None, None])
    
    normalized_df = normalize_dates(df, ['date_col'])
    
    pd.testing.assert_series_equal(normalized_df['date_col'], expected_dates)