#!/usr/bin/env python

from abc import ABC, abstractmethod
from genecodata.rdf_handlers.triples_classes import RDFTriple, RDFTriplesSet

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

	def write_triple(self, triple:RDFTriple, endline:str=".", linejump=False):
		"""Write a triple in a turtle (.ttl) file"""

		with open(self.file, "a") as f:
			f.write(f"""{triple.subject} {triple.predicate} {triple.object} {endline}\n""")

			if linejump:
				f.write("\n")

	def write_tripleset(self, rdf_triple_set:RDFTriplesSet):
		"""Write a set of triples with the same subject in a turtle (.ttl) file """

		with open(self.file, "a") as f:

			f.write(rdf_triple_set.subject)

			for triple in rdf_triple_set[0:-1]:
				f.write(f"""\t {triple.predicate}: <{triple.object}> ;\n""")
			
			f.write(f"""\t {rdf_triple_set[-1].predicate}: <{rdf_triple_set[-1].object}> ;\n""")
			f.write("\n")
