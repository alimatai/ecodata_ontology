#!/usr/bin/env python

import logger

class RDFTriple():

	def __init__(self):
		self.subject = None
		self.predicate = None
		self.object = None

	def __init__(self, sub:str, pred:str, obj:str):
		# TODO : warning if no prefix
		self.subject = sub
		self.predicate = pred
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

	@subject.setter
	def subject(self, value):
		self._subject = value

	@predicate.setter
	def predicate(self, value):
		self._predicate = value

	@object.setter
	def object(self, value):
		self._object = value

	def __str__(self, end:str=".") -> str:
		return f"""{self.subject} {self.predicate} {self.object} {end}"""

	def tolist(self) -> list:
		return [self.subject, self.predicate, self.object]

	def write(self, file, mode, end:str="."):
		with open(file, mode) as f:
			f.write(self.__str__())
			f.write("\n")

	# def modify_end(self) -> str:
	# 	self.end = {".":";", ";":"."}[self.end]

class RDFTriplesSet():
	"""Gather triples with a common subject"""

	def __init__(self, triples:list[RDFTriple]):
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

	def write(self, file, mode:str):
		"""Write a set of triples with the same subject in a turtle (.ttl) file. The file will be updated or overwritten depending on the value of the mode parameter"""
		if mode not in {"w", "a"}:
			raise ValueError("mode must be one of {\"w\", \"a\"}")

		with open(file, mode) as f:
			f.write(self.__str__())
