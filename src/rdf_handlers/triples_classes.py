#!/usr/bin/env python

from abc import ABC, abstractmethod
import logger

class RDFTriple(ABC):

	def __init__(self, sub, pred, obj):
		self.subject = sub
		self.predicate = pred
		self.object = obj

	@abstractmethod
	def __str__(self, end:str=".") -> str:
		pass

	@abstractmethod
	def tolist(self) -> list:
		pass

	@abstractmethod
	def write():
		pass

class TurtleTriple(RDFTriple):

	def __init__(self):
		self.sub = None
		self.pred = None
		self.obj = None

	def __init__(self, sub:str, pred:str, obj:str):
		# TODO : warning if no prefix
		self.sub = sub
		self.pred = pred
		self.obj = obj

	@property
	def sub(self):
		return self._sub

	@property
	def pred(self):
		return self._pred

	@property
	def obj(self):
		return self._obj

	@sub.setter
	def sub(self, value):
		self._sub = value

	@pred.setter
	def pred(self, value):
		self._pred = value

	@obj.setter
	def obj(self, value):
		self._obj = value

	def __str__(self, end:str=".") -> str:
		return f"""{self.sub} {self.pred} {self.obj} {end}"""

	def tolist(self) -> list:
		return [self.sub, self.pred, self.obj]

	def write(self, openfile):
		openfile.write(self.__str__)

	# def modify_end(self) -> str:
	# 	self.end = {".":";", ";":"."}[self.end]

class RDFTriplesSet(ABC):

	def __init__(self, triples:list[RDFTriple]):
		pass

	@abstractmethod
	def __str__(self):
		pass

	@abstractmethod
	def write(self, outfile, mode:str):
		pass

class TurtleTripleSet(RDFTriplesSet):
	"""Gather triples with a common subject"""

	def __init__(self, triples:list[TurtleTriple]):
		"""Initialize the set of triples ; verifies if all subjects are the same"""
		try:
			if len(set([triple.sub for triple in triples])) == 1:
				self.sub = triples[0].sub
				self.pred_obj_pairs = [(triple.pred, triple.obj) for triple in triples]

		except ValueError as e:
			logger.error(f"Error : triples do not have the same subject: {e}")

	def __str__(self):
		output = f"""{self.sub} {self.pred_obj_pairs[0][0]} {self.pred_obj_pairs[0][1]} ;\n"""

		for pair in self.pred_obj_pairs[:-1]:
			output += f"""\t{pair[0]} {pair[1]} ;\n"""

		output += f"""\t{self.pred_obj_pairs[-1][0]} {self.pred_obj_pairs[-1][0]} .\n\n"""

		return output

	@property
	def sub(self):
		return self._sub

	@property
	def pred_obj_pairs(self):
		return self._pred_obj_pairs

	@sub.setter
	def sub(self, value):
		self._sub = value

	@pred_obj_pairs.setter
	def pred_obj_pairs(self, value):
		self._pred_obj_pairs = value

	def write(self, outfile, mode:str):
		"""Write a set of triples with the same subject in a turtle (.ttl) file. The file will be updated or overwritten depending on the value of the mode parameter"""
		if mode not in {"w", "a"}:
			raise ValueError("mode must be one of {\"w\", \"a\"}")

		with open(outfile, mode) as f:
			f.write(self.__str__())
