__all__ = ("parseLine", "parseSourceList")

import typing
from pathlib import Path
import _io

from UniGrammarRuntime.ParserBundle import ParserBundle


thisFile = Path(__file__).absolute()
thisDir = thisFile.parent
bundleDir = thisDir / "parserBundle"

bundle = ParserBundle(bundleDir)

grammar = bundle.grammars["apt_source"]
wrapper = grammar.getWrapper("parglare")


parseLine = wrapper


defaultSourceList = None

def getDefaultSourceList():
	global defaultSourceList
	
	if defaultSourceList is not None:
		return defaultSourceList
	
	try:
		from fuckapt import sourcesListFile
		defaultSourceList = sourcesListFile
	except ImportError:
		defaultSourceList = Path("/etc/apt/sources.list")
	
	return defaultSourceList


def parseSourceList(lst: typing.Union[str, Path, _io._TextIOBase] = None):
	"""Parses whole `sources.list`"""
	if lst is None:
		lst = getDefaultSourceList()

	if isinstance(lst, str):
		lines = lst.splitlines()
	elif isinstance(lst, Path):
		lines = lst.open("rt", encoding="utf-8")
	elif isinstance(lst, _io._TextIOBase):
		lines = lst
	else:
		raise ValueError("`lst` has wrong type")

	for l in lines:
		l = l.strip()
		if l:
			parsed = parseLine(l)
			yield parsed
		else:
			yield ""
