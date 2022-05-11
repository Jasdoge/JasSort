try:
	from .jas_sort_action import JasSort
	JasSort().register()
except Exception as e:
	import os
	plugin_dir = os.path.dirname(os.path.realpath(__file__))
	log_file = os.path.join(plugin_dir, 'Replicate_layout_error.log')
	with open(log_file, 'w') as f:
		f.write(repr(e))
