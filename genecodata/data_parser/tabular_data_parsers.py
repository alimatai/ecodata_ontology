#!/usr/bin/env python

from abc import ABC, abstractmethod
import pandas as pd

# TODO : un linter du tableau de config pour repérer les erreurs ?

class TableParser(ABC):

	def __init__(self, path):
		pass

	# @abstractmethod
	# def __load():
	# 	pass

class TxtParser(TableParser):

	def __init__(self, path, sep):
		# self.table = self.__load(path, sep)
		self.path = path
		self.sep = sep
		self.table = pd.read_csv(path, index_col=0, header=0, sep=sep)

	@property
	def path(self):
		return self._path
	
	@property
	def sep(self):
		return self._sep
	
	@property
	def table(self):
		return self._table
	
	@path.setter
	def path(self, value):
		self._path = value

	@sep.setter
	def sep(self, value):
		self._sep = value
	
	@table.setter
	def table(self, value):
		self._table = value

	# def __load(self, path, sep):
	# 	self.table = pd.read_csv(path, index_col=0, header=0, sep=sep)

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

