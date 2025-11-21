import pytest
import pandas as pd
from Transform.enrichment import enrich_data

def test_enrich_data():
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10, 20, 30]
    })
    
    additional_data = pd.DataFrame({
        'id': [1, 2],
        'extra_value': [100, 200]
    })
    
    enriched_df = enrich_data(df, additional_data, on='id')
    
    expected_df = pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10, 20, 30],
        'extra_value': [100, 200, None]
    })
    
    pd.testing.assert_frame_equal(enriched_df, expected_df)