class Record:
	"""Represents a single line in sources.list mentioning a source."""
	__slots__ = ("commented", "type", "options", "schemaModifiers", "uri", "distribution", "components")

	def __init__(self):
		self.commented = None
		self.type = None
		self.options = None
		self.uri = None
		self.distribution = None
		self.components = None
		self.schemaModifiers = None

	def serializeOptions(self) -> str:
		if self.options:
			return "[" + ",".join(k + "=" + v for k, v in self.options.items()) + "]"
		return ""

	def serializeComponents(self) -> str:
		if self.components:
			return " ".join(self.components)
		return ""

	def __str__(self) -> str:
		return " ".join(filter(None, ("#" if self.commented else "", self.type, self.serializeOptions(), "+".join(self.schemaModifiers + [self.uri,]), self.distribution, self.serializeComponents())))

	def __repr__(self) -> str:
		return self.__class__.__name__ + "(" + repr(str(self)) + ")"
