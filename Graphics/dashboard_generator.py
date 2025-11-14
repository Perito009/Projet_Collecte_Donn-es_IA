def generate_dashboard(df_html, output_path):
	"""
	Prend du HTML (ex: df.to_html()) ou une string et écrit dashboard minimal.
	"""
	template = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Dashboard</title></head>
<body>
<h1>Dashboard</h1>
{df_html}
</body></html>"""
	with open(output_path, "w", encoding="utf-8") as f:
		f.write(template)
