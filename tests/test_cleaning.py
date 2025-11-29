# tests/test_cleaning_advanced.py
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from Transform.data_cleaning import detect_outliers

class TestDataCleaningAdvanced:
    
    def test_detect_outliers_realistic(self):
        """Test avec des données plus réalistes"""
        # Créer une distribution normale avec quelques outliers
        np.random.seed(42)  # Pour la reproductibilité
        
        # Données normales pour T001
        normal_data = np.random.normal(100, 10, 20)  # Moyenne 100, écart-type 10
        
        # Ajouter quelques outliers
        outlier_data = [500, 600]  # Valeurs clairement aberrantes
        
        # Combiner les données
        all_data = list(normal_data) + outlier_data
        turbin_ids = ['T001'] * len(all_data)
        
        df = pd.DataFrame({
            'turbin_id': turbin_ids,
            'energie_kWh': all_data
        })
        
        # Appliquer la détection
        df_result = detect_outliers(df)
        
        # Vérifier que les outliers sont détectés
        outliers_detected = df_result['energy_anomaly'].sum()
        print(f"Outliers détectés: {outliers_detected}")
        
        # Doit détecter au moins les 2 outliers évidents
        assert outliers_detected >= 2
        
        # Vérifier que les valeurs 500 et 600 sont marquées comme outliers
        outlier_500 = df_result[df_result['energie_kWh'] == 500]
        outlier_600 = df_result[df_result['energie_kWh'] == 600]
        
        if not outlier_500.empty:
            assert outlier_500['energy_anomaly'].iloc[0] == True
        if not outlier_600.empty:
            assert outlier_600['energy_anomaly'].iloc[0] == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])