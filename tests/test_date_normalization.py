# tests/test_date_normalization.py
import pytest
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from Transform.date_normalization import normalize_timestamp_column

class TestDateNormalization:
    
    def test_normalize_timestamp_valid(self):
        """Test la normalisation de timestamps valides"""
        # Créer des timestamps de test
        df = pd.DataFrame({
            'ts_utc': [
                '2024-01-01 10:00:00+00:00',
                '2024-01-01 11:00:00+00:00'
            ]
        })
        
        # Appliquer la normalisation
        df_result = normalize_timestamp_column(df, 'ts_utc')
        
        # Vérifier que les timestamps sont normalisés
        assert len(df_result) == 2
        assert '+0100' in df_result['ts_utc'].iloc[0]  # Doit être en Europe/Paris
        assert '2024-01-01T' in df_result['ts_utc'].iloc[0]  # Format ISO
    
    def test_normalize_timestamp_invalid(self):
        """Test avec des timestamps invalides"""
        # Créer des données avec un timestamp invalide
        df = pd.DataFrame({
            'ts_utc': [
                '2024-01-01 10:00:00',  # Valide
                'invalid_date',          # Invalide
                None                     # Null
            ]
        })
        
        # Appliquer la normalisation
        df_result = normalize_timestamp_column(df, 'ts_utc')
        
        # Vérifier que la fonction gère les erreurs
        assert len(df_result) == 3  # Même nombre de lignes
        # Au moins un timestamp devrait être valide
        assert df_result['ts_utc'].notna().sum() >= 1
    
    def test_missing_column(self):
        """Test quand la colonne timestamp n'existe pas"""
        df = pd.DataFrame({
            'other_column': [1, 2, 3]
        })
        
        # Devrait retourner le DataFrame sans erreur
        df_result = normalize_timestamp_column(df, 'ts_utc')
        assert len(df_result) == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])