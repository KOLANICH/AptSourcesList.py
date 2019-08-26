import typing
from UniGrammarRuntime.IWrapper import IWrapper, IParseResult


class record(IParseResult):
	__slots__ = ("commented", "rType", "options", "uri", "distribution", "components")

	def __init__(self):
		self.commented = None
		self.rType = None
		self.options = None
		self.uri = None
		self.distribution = None
		self.components = None


class component(IParseResult):
	__slots__ = ("cId",)

	def __init__(self):
		self.cId = None


class optionsR(IParseResult):
	__slots__ = ("pairs",)

	def __init__(self):
		self.pairs = None


class optionR(IParseResult):
	__slots__ = "key", "value"

	def __init__(self):
		self.key = None
		self.value = None


class recordParser(IWrapper):
	__slots__ = ()

	def process_record(self, parsed) -> record:
		rec = record()
		rec.commented = self.process_commenterROpt(parsed.commented)
		rec.rType = self.backend.terminalNodeToStr(parsed.rType)
		rec.options = self.process_optionsOpt(parsed.options)
		rec.uri = self.backend.getSubTreeText(parsed.uri)
		rec.distribution = self.backend.getSubTreeText(parsed.distribution)
		rec.components = self.process_componentsR(parsed.components)
		return rec

	def process_component(self, parsed) -> component:
		rec = component()
		rec.cId = self.backend.getSubTreeText(parsed.cId)
		return rec

	def process_componentsR_(self, parsed) -> typing.Iterable[component]:
		for f in self.backend.iterateCollection(parsed):
			yield f

	def process_componentsR(self, parsed):
		return [self.process_component(f) for f in self.process_componentsR_(parsed)]

	def process_optionsOpt(self, parsed) -> typing.Optional[optionsR]:
		if parsed is not None:
			return self.process_optionsR(parsed)

	def process_optionsR(self, parsed) -> optionsR:
		rec = optionsR()
		rec.pairs = self.process_delimited_optionR(parsed.pairs)
		return rec

	def process_delimited_optionR_(self, parsed) -> typing.Iterable[optionR]:
		yield parsed.first_option
		for f in self.backend.iterateCollection(parsed.rest_options_with_del):
			yield f.rest_option

	def process_delimited_optionR(self, parsed):
		return [self.process_optionR(f) for f in self.process_delimited_optionR_(parsed)]

	def process_optionR(self, parsed) -> optionR:
		rec = optionR()
		rec.key = self.backend.terminalNodeToStr(parsed.key)
		rec.value = self.backend.getSubTreeText(parsed.value)
		return rec

	def process_commenterROpt(self, parsed) -> typing.Optional[str]:
		if parsed is not None:
			return self.backend.getSubTreeText(parsed)

	__MAIN_PRODUCTION__ = process_record


__MAIN_PARSER__ = recordParser
