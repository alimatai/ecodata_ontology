#!/usr/bin/env python

from abc import ABC, abstractmethod
# import pandas as pd
import datatable as dt
import json

# TODO : un linter du tableau de config pour repérer les erreurs ?

class TableParser(ABC):

	def __init__(self, path, configfile):
		self.path = path
		self.configfile = configfile

	@abstractmethod
	def load():
		pass

class TxtParser(TableParser):

	def __init__(self, path, sep, **kwargs):
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
		self.table = dt.fread(path, sep=self.sep)

class ExcelParser(TableParser):

	def __init__(self, path, sheet, configfile, **kwargs):
		self.path = path
		self.sheet = self.__load(path, sheet)
		self.configfile = configfile

	@property
	def path(self):
		return self._path

	@property
	def sheet(self):
		return self._sheet
	
	@property
	def configfile(self):
		return self._configfile
	
	
	def __load(self):
		self.table = pd.read_excel(self.path, index_col=0, header=0, sheet=self.sheet)

