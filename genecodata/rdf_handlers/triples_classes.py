#!/usr/bin/env python

import abc
import logger

class Prefix():
	"""Defines a rdf prefix with its abbreviation and its full URI"""

	def __init__(self, abbr:str, uri:str):
		self.abbr = abbr
		self.uri = uri

	@property
	def abbr(self):
		return self._abbr
	
	@property
	def uri(self):
		return self._uri
	
	@abbr.setter
	def abbr(self, value):
		self._abbr = value

	@uri.setter
	def uri(self, value):
		self._uri = value


class RDFelem(abc.ABC):
	"""Abstract class for more precise RDF constituants"""

	def __init__(self, name:str, prefix:Prefix):
		self.name = name
		self.prefix = prefix

	@property
	def name(self):
		return self._name
	
	@property
	def prefix(self):
		return self._prefix

	@name.setter
	def name(self, value):
		self._name = value

	@prefix.setter
	def prefix(self, value):
		self._prefix = value
	

class RDFNode(RDFelem):
	"""Used as a subject or an object in a RDF triple"""

	def __init__(self, name:str, prefix:Prefix):
		self.name = name
		self.prefix = prefix

	@property
	def name(self):
		return self._name
	
	@property
	def prefix(self):
		return self._prefix

	@name.setter
	def name(self, value):
		self._name = value

	@prefix.setter
	def prefix(self, value):
		self._prefix = value

class Predicate(RDFelem):
	"""Defines the predicate linking a subject to an object"""

	def __init__(self, name:str, prefix:Prefix):
		self.name = name
		self.prefix = prefix

	@property
	def name(self):
		return self._name
	
	@property
	def prefix(self):
		return self._prefix

	@name.setter
	def name(self, value):
		self._name = value

	@prefix.setter
	def prefix(self, value):
		self._prefix = value

class RDFTriple():

	def __init__(self, subject:RDFNode, predicate:Predicate, obj:RDFNode):
		self.subject = subject
		self.predicate = predicate
		self.object = obj

	@property
	def subject(self):
		return self._subject
	
	@property
	def predicate(self):
		return self._predicate
	
	@property
	def object(self):
		return self._object	

	def __str__(self) -> str:
		return f"""{self.subject} {self.predicate} {self.object}"""

	def tolist(self) -> list:
		return [self.subject, self.predicate, self.object]

class RDFTriplesSet():

	def __init__(self, subject:RDFNode):
		"""Initiates only the subject and an empty list of predicate / object couples"""
		self.subject = subject
		self.predicates_objects_couples = []

	def __init__(self, subject:RDFNode, predicates_objects_couples:list[tuple]):
		"""Initiates the subject and the list of predicate / object couples"""
		self.subject = subject
		self.predicates_objects_couples = predicates_objects_couples

	def __init__(self, triples:list[RDFTriple]):
		"""Initiates everything from a list of triples"""
		try:
			if len(set([triple.sub for triple in triples])) == 1:
				self.sub = triples[0].sub
				self.pred_obj_pairs = [(triple.pred, triple.obj) for triple in triples]

		except ValueError as e:
			logger.error(f"Error : triples of the input list do not have the same subject: {e}")

	@property
	def subject(self):
		return self._subject
	
	@property
	def predicates_objects_couples(self):
		return self._predicates_objects_couples

	@predicates_objects_couples.setter
	def predicates_objects_couples(self, value):
		self._predicates_objects_couples = value

	def add_couple(self, triple:RDFTriple):
		try:
			if triple.subject == self.subject:
				self.predicates_objects_couples.append((triple.predicate, triple.object))

		except ValueError as e:
			logger.error(f"Error : the triple to add do not have the correct subject: {e}")

	def __str__(self):
		output = f"""{self.subject} {self.predicates_objects_couples[0][0]} {self.predicates_objects_couples[0][1]} ;\n"""

		for pair in self.predicates_objects_couples[:-1]:
			output += f"""\t{pair[0]} {pair[1]} ;\n"""

		output += f"""\t{self.predicates_objects_couples[-1][0]} {self.predicates_objects_couples[-1][0]} .\n\n"""

		return output