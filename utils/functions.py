import os

def check_type(instance, instance_type):
	if not isinstance(instance, instance_type):
		raise ValueError(f'Given object is not an instance of {instance_type.__name__}')

def clear_screen():
	os.system('cls' if os.name=='nt' else 'clear')

def pretty_text_format(text):
	return ' '.join(text.strip().split())

def avg(arr):
	if len(arr) == 0:
		raise ValueError('Cannot accept empty array')
	return sum(arr) / len(arr)