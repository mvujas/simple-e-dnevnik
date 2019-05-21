import config

def debug_print(*params):
	if config.DEBUG:
		print('------------------------------\nDEBUG:', 
			*params, 
			'\n------------------------------')