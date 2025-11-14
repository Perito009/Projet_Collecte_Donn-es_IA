from pipeline import main

def test_pipeline_dry_run():
	"""
	Vérifie que main(dry_run=True) s'exécute et renvoie True.
	"""
	assert main(dry_run=True) is True
