import typing
from abc import ABC, abstractmethod
from .Record import Record

class RecordParser(ABC):
	"""A class commanding the parsing. Calls the generated parser and postporcesses its output"""
	__slots__ = ()

	EX_CLASS = Exception

	@abstractmethod
	def iterateList(self, lst):
		raise NotImplementedError()
	
	@abstractmethod
	def isList(self, lst):
		raise NotImplementedError()

	@abstractmethod
	def parseURI(self, rec, uri):
		raise NotImplementedError()

	def mergeShit(self, lst: typing.Any) -> str:
		res = []
		stack = []
		if self.isList(lst):
			for t in self.iterateList(lst):
				res.append(self.mergeShit(t))
		else:
			res.append(self.getTextFromToken(lst))
		return "".join(res)

	def descendIntoURISchema(self, schema: typing.Any) -> typing.Iterator[str]:
		restWords = schema
		yield self.getTextFromToken(schema.word)
		if schema.restWords:
			for w in self.iterateList(schema.restWords):
				res = self.getTextFromToken(w.word)
				yield res

	def __call__(self, s: str) -> Record:
		rec = Record()
		parsed = self.parse(s)
		
		try:
			commented = bool(self.getTextFromToken(parsed.commented))
		except:
			commented = False
		
		rec.commented = commented
		rec.type = self.getTextFromToken(parsed.rType)
		rec.options = parsed.options
		rec.uri = parsed.uri
		rec.distribution = self.mergeShit(parsed.distribution)
		rec.components = parsed.components
		rec.schemaModifiers = None
		
		if rec.uri:
			rec.uri = self.parseURI(rec, rec.uri)

		if rec.options:
			if rec.options.pairs:
				pairs = rec.options.pairs
				res = [pairs.firstOption]
				
				try:
					restOptions = pairs.restOptions
				except:
					restOptions = []
				
				for p in self.iterateList(restOptions):
					res.append(p.option)
				
				rec.options = res
				rec.options = {self.getTextFromToken(p.key): self.mergeShit(p.value) for p in rec.options}

		if rec.components:
			rec.components = [self.mergeShit(c.cId) for c in self.iterateList(rec.components)]
		return rec

