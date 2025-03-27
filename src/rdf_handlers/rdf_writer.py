#!/usr/bin/env python

from abc import ABC, abstractmethod

class RDFWriter(ABC):

	def __init__(self, prefixlist):
		pass

	@abstractmethod
	def write_prefixes(self):
		pass

	@abstractmethod
	def write_tripleset(self):
		pass

class TurtleWriter(RDFWriter):

	def __init__(self, prefixdict, file):
		self.prefixdict = prefixdict
		self.file = file

	@property
	def prefixdict(self):
		"""Prefixes getter"""
		return self._prefixdict
	
	@property
	def file(self):
		"""Output file name getter"""
		return self._file
	
	@prefixdict.setter
	def prefixdict(self, value):
		"""Prefixes setter"""
		self._prefixdict = value

	@file.setter
	def file(self, value):
		"""Output file name setter"""
		self._file = value

	def write_prefixes(self):
		"""Write the prefixes list in a turtle (.ttl) file (non-empty file will be overwritten)"""
		
		with open(self.file, "w") as f:
			for prefix, uri in self.prefixdict.items():
				f.write(f"""@prefix {prefix}: <{uri}> .\n""")
			f.write("\n")

	def write_tripleset(self, TurtleTripleSet):
		"""Write a set of triples with the same subject in a turtle (.ttl) file """
		TurtleTripleSet.write(self.file, "a")
