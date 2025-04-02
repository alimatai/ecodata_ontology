#!/usr/bin/env python

from abc import ABC, abstractmethod
import pandas as pd

# TODO : un linter du tableau de config pour repérer les erreurs ?

class TableParser(ABC):

	def __init__(self, path):
		self.path = path

	@abstractmethod
	def load():
		pass

class TxtParser(TableParser):

	def __init__(self, path, sep):
		self.path = path
		self.sep = sep
		self.table = self.__load(path, sep)

	@property
	def path(self):
		return self._path
	
	@property
	def sep(self):
		return self._sep
	
	@property
	def table(self):
		return self._table

	def __load(self, path):
		self.table = pd.read_csv(path, index_col=0, header=0, sep=self.sep)

class ExcelParser(TableParser):

	def __init__(self, path, sheet):
		self.path = path
		self.table = self.__load(path, sheet)

	def __init__(self, path, sheet, metadatasheet):
		self.path = path
		self.table = self.__load(path, sheet)
		self.metadata = self.load(path, metadatasheet)

	@property
	def path(self):
		return self._path

	@property
	def sheet(self):
		return self._sheet
	
	@property
	def table(self):
		return self._table
	
	@property
	def metadata(self):
		return self._metadata
	
	def __load(self):
		self.table = pd.read_excel(self.path, index_col=0, header=0, sheet=self.sheet)

