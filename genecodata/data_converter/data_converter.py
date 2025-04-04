#!/usr/bin/env python

from genecodata.data_parser.tabular_data_parsers import TableParser
from genecodata.rdf_handlers.triples_classes import TurtleTriple
from abc import ABC
import pandas as pd

class DataConverter(ABC):

	def __init__(self,  project_prefix:str, data:TableParser,):
		self.project_prefix = project_prefix
		self.data = data		

class ConfigTurtleConverter(DataConverter):
	"""Convert Config data loaded in a TableParser object into RDF triples"""

	def __init__(self, project_prefix:str, data:TableParser):
		self.project_prefix = project_prefix
		self.data = data # The config file of the project

	@property
	def project_prefix(self):
		return self._project_prefix
	
	@property
	def data(self):
		return self._data
	
	@project_prefix.setter
	def project_prefix(self, value):
		self._project_prefix = value

	@data.setter
	def data(self, value):
		self._data = value

	def observable_properties_triples(self):
		"""Parse config table and set up triples of sosa:ObservableProperties"""
		# triples = [TurtleTriple()] * self.data.dim[0]
		# n = 0

		df = self.data.table.loc[self.data.table["Type"]=="ObservableProperty"]

		triples = []

		for index, row in df.iterrows():
			triples.append(TurtleTriple(
				f"""{self.project_prefix}:{row["InDbName"]}""", 
				"rdf:type", 
				"sosa:Observableproperty")
			)
			triples.append(
				TurtleTriple(
					f"""{self.project_prefix}:{row["InDbName"]}""", 
					"rdf:type", 
					"iop:Variable"))

			if row["AltURI"] != "":
				for uri in row["AltURI"].split(","):
					triples.append(
						TurtleTriple(
							f"""{self.project_prefix}:{row["InDbName"]}""", 
							"rdf:type", 
							f"""{uri}"""
						)
					)

			if row["Set"] != "":
				triples.append(
					TurtleTriple(
						f"""{self.project_prefix}:{row["Set"]}""", 
						"iop:hasMember", 
						f"""{self.project_prefix}:{row["InDbName"]}"""
					)
				)

		return triples

	def features_of_interest_triples(self):
		"""Parse config table and set up triples of sosa:FeaturesOfInterest"""

		df = self.data.table.loc[self.data.table["Type"]=="FeatureOfInterest"]

		triples = []
		for index, row in df.iterrows():
			triples.append(
				TurtleTriple(
					f"""{self.project_prefix}:{row["InDbName"]}""", 
					"rdf:type", 
					"sosa:FeatureOfInterest"
				)
			)

			if row["AltURI"] != "No URI":
				for uri in row["AltURI"].split(","):
					triples.append(
						TurtleTriple(
							f"""{self.project_prefix}:{row["InDbName"]}""", 
							"rdf:type", 
							f"""{uri}"""
						)
					)
	
	def variablesets_triples(self):
		"""Parse config file and set up triples of variable sets"""

		varsets = self.data.table["Set"].unique()
		varsets.dropna(inplace=True)

		triples = []

		for varset in varsets:
			triples.append(
				TurtleTriple(
					f"""{self.project_prefix}:{varset}""", 
					"rdf:type", 
					"iop:VariableSet"
				)
			)

		pass