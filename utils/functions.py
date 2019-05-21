def check_type(instance, instance_type):
	if not isinstance(instance, instance_type):
		raise ValueError(f'Given object is not an instance of {instance_type.__name__}')