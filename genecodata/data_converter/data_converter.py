#!/usr/bin/env python

from genecodata.data_parser.tabular_data_parsers import TableParser
from genecodata.rdf_handlers.triples_classes import RDFTriple
import pandas as pd

class ConfigTurtleConverter():
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

		df = self.data.table.loc[self.data.table["Type"]=="sosa:ObservableProperty"]
		triples = []

		for index, row in df.iterrows():
			triples.append(
				RDFTriple(
					f"""{self.project_prefix}:{row["InDbName"]}""", 
					"rdf:type", 
					"sosa:Observableproperty"
				)
			)
			triples.append(
				RDFTriple(
					f"""{self.project_prefix}:{row["InDbName"]}""", 
					"rdf:type", 
					"iop:Variable")
				)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					triples.append(
						RDFTriple(
							f"""{self.project_prefix}:{row["InDbName"]}""", 
							"rdf:type", 
							f"""{uri}"""
						)
					)

			if not pd.isna(row["Set"]):
				triples.append(
					RDFTriple(
						f"""{self.project_prefix}:{row["Set"]}""", 
						"iop:hasMember", 
						f"""{self.project_prefix}:{row["InDbName"]}"""
					)
				)

		return triples

	def features_of_interest_triples(self):
		"""Parse config table and set up triples of sosa:FeaturesOfInterest"""

		df = self.data.table.loc[self.data.table["Type"]=="sosa:FeatureOfInterest"]
		
		triples = []
		for index, row in df.iterrows():
			triples.append(
				RDFTriple(
					f"""{self.project_prefix}:{row["InDbName"]}""", 
					"rdf:type", 
					"sosa:FeatureOfInterest"
				)
			)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					triples.append(
						RDFTriple(
							f"""{self.project_prefix}:{row["InDbName"]}""", 
							"rdf:type", 
							f"""{uri}"""
						)
					)

		return triples
	
	def variablesets_triples(self):
		"""Parse config file and set up triples of variable sets"""

		varsets = self.data.table["Set"].dropna().unique()

		triples = []

		for varset in varsets:
			triples.append(
				RDFTriple(
					f"""{self.project_prefix}:{varset}""", 
					"rdf:type", 
					"iop:VariableSet"
				)
			)

		return triples
