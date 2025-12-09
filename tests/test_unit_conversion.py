# tests/test_unit_conversion.py
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from Transform.unit_conversion import normalize_units, celsius_to_kelvin, kmh_to_ms

class TestUnitConversion:
    
    def test_celsius_to_kelvin(self):
        """Test la conversion Celsius vers Kelvin"""
        # Test valeur normale
        assert celsius_to_kelvin(25) == 298.15
        # Test zéro
        assert celsius_to_kelvin(0) == 273.15
        # Test valeur négative
        assert celsius_to_kelvin(-10) == 263.15
        # Test valeur manquante
        assert celsius_to_kelvin(np.nan) is None
    
    def test_kmh_to_ms(self):
        """Test la conversion km/h vers m/s"""
        # Test valeur normale
        assert kmh_to_ms(36) == 10.0
        # Test zéro
        assert kmh_to_ms(0) == 0.0
        # Test valeur manquante
        assert kmh_to_ms(np.nan) is None
    
    def test_normalize_units_complete(self):
        """Test la normalisation complète des unités"""
        # Créer des données avec toutes les colonnes à convertir
        df = pd.DataFrame({
            'temperature': [20, 25, 30],
            'wind_speed': [36, 72, 18],
            'energie_kWh': [1000, 2000, 1500]
        })
        
        # Appliquer les conversions
        df_result = normalize_units(df)
        
        # Vérifier les nouvelles colonnes
        assert 'temperature_K' in df_result.columns
        assert 'wind_speed_ms' in df_result.columns
        assert 'energie_mwh' in df_result.columns
        
        # Vérifier les conversions
        assert df_result['temperature_K'].iloc[0] == 293.15  # 20°C → 293.15K
        assert df_result['wind_speed_ms'].iloc[0] == 10.0    # 36 km/h → 10 m/s
        assert df_result['energie_mwh'].iloc[0] == 1.0       # 1000 kWh → 1 MWh
    
    def test_normalize_units_partial(self):
        """Test avec seulement certaines colonnes présentes"""
        # Données avec seulement température
        df = pd.DataFrame({
            'temperature': [10, 20, 30]
        })
        
        df_result = normalize_units(df)
        
        # Doit avoir la colonne température convertie
        assert 'temperature_K' in df_result.columns
        # Ne doit pas avoir les autres colonnes de conversion
        assert 'wind_speed_ms' not in df_result.columns

if __name__ == "__main__":
    pytest.main([__file__, "-v"])