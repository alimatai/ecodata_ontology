#!/usr/bin/env python

from abc import ABC, abstractmethod
import pandas as pd

# TODO : un linter du tableau de config pour repérer les erreurs ?

class TableParser(ABC):

	def __init__(self, path):
		pass

class TxtParser(TableParser):

	def __init__(self, path, sep):
		self.table = pd.read_csv(path, index_col=0, header=0, sep=sep)
	
	@property
	def table(self):
		return self._table
	
	@table.setter
	def table(self, value):
		self._table = value

class ExcelParser(TableParser):

	def __init__(self, path, sheet:int):
		self.table = self.__load(path, sheet)

	def __init__(self, path, sheet:int, metadatasheet:int):
		self.table = pd.read_excel(path, index_col=0, header=0, sheet=sheet)
		self.metadata = pd.read_excel(path, index_col=0, header=0, sheet=metadatasheet)

	@property
	def table(self):
		return self._table
	
	@property
	def metadata(self):
		return self._metadata

