class ObjectPool:
	def __init__(self, instance_type, start_size=5, max_size=None):
		start_size = max(0, start_size)
		if max_size is not None:
			max_size = max(0, max_size)
		if max_size is not None and start_size > max_size:
			raise ValueError('Starting size of object pool must be less than its maximum size')
		self.__instance_type = instance_type
		self.__maximum_size = max_size

		self.__instances = [self.__instance_type() for i in range(start_size)]
		self.__in_use = []

	def get(self):
		instance = None
		if len(self.__instances) == 0:
			if self.is_empty():
				raise ValueError('Object pool is empty')
			instance = self.__instance_type()
		else:
			instance = self.__instances.pop()
		self.__in_use.append(instance)
		return instance

	def release(self, instance):
		try:
			self.__in_use.remove(instance)
		except:
			raise ValueError('Given instance is not in use')
		self.__instances.append(instance)

	@property
	def size(self):
		return len(self.__instances) + len(self.__in_use)

	@property
	def instance_type(self):
		return self.__instance_type

	def is_empty(self):
		return self.__maximum_size is not None and self.size == self.__maximum_size