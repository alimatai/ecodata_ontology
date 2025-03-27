#!/usr/bin/env python

from abc import ABC, abstractmethod
import pandas as pd
import json

class TableParser(ABC):

	def __init__(self, path, configfile):
		self.path = path
		self.configfile = configfile

	@abstractmethod
	def load():
		pass

class TxtParser(TableParser):

	def __init__(self, path, sep, configfile, **kwargs):
		self.path = path
		self.sep = sep
		self.configfile = json.load(configfile)

		self.table = self.__load(path, sep)

	def __load(self, path, sep):
		self.table = pd.read_csv(path, index_col=0, header=0, sep=sep)

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

