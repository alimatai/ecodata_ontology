#!/usr/bin/env python

from genecodata.data_parser.tabular_data_parsers import TableParser, ExcelParser
# from genecodata.rdf_handlers.triples_classes import RDFTriple
import pandas as pd

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

import logger

class PrefixesBinder():

	def __init__(self, project_prefixes:pd.DataFrame):
		try:
			if not project_prefixes.columns == ("Prefix","URI"):
				self.project_prefixes = project_prefixes
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_prefixes.tsv: {e}")

	@property
	def project_prefixes(self):
		return self._project_prefixes	

	@project_prefixes.setter
	def project_prefixes(self, value):
		self._project_prefixes = value

	def bind_prefixes(self, g:Graph):
		"""Parse all the prefixes and bind them to the graph g"""

		for index, row in self.project_prefixes.iterrows():
			g.bind(index, row["URI"])


class ObservablePropertiesConverter():
	"""Convert Config data loaded in a TableParser object into RDF triples"""

	def __init__(self, obs_props:pd.DataFrame):
		try:
			if not obs_props.columns == ("Name","InDbName","AltURI","Set", "Unit","DataType"):
				self.obs_props = obs_props
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_variables.tsv: {e}")

	@property
	def obs_props(self):
		return self._obs_props

	@obs_props.setter
	def obs_props(self, value):
		self._obs_props = value

	def observable_properties_triples(self, g:Graph):
		"""Parse config table and set up triples of sosa:ObservableProperties"""

		for _, row in self.obs_props.iterrows():
			g.add(
				(
					# URIRef(f"""{self.project_prefix}:{row["InDbName"]}"""), 
					URIRef(f"""{row["InDbName"]}"""),					
					RDF.type, 
					URIRef("http://www.w3.org/ns/sosa/Observableproperty")
				)
			)
			g.add(
				(
					# URIRef(f"""{self.project_prefix}:{row["InDbName"]}"""),
					URIRef(f"""{row["InDbName"]}"""),
					RDF.type,
					URIRef("https://w3id.org/iadopt/ont/Variable")
				)
			)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					#obj = self.project_prefixes.loc[uri.split(":")[0], "uri"]
					g.add(
						(
							# URIRef(f"""{self.project_prefix}:{row["InDbName"]}"""), 
							URIRef(f"""{row["InDbName"]}"""),
							RDF.type,
							URIRef(f"{uri}")
						)
					)

			if not pd.isna(row["Set"]):
				g.add(
					(
						URIRef(f"""{row["Set"]}"""), 
						URIRef("https://w3id.org/iadopt/ont/hasMember/"),
						URIRef(f"""{row["InDbName"]}""")
						# URIRef(f"""{self.project_prefix}:{row["InDbName"]}""")
					)
				)
	
	def variablesets_triples(self, g:Graph):
		"""Parse config file and set up triples of variable sets"""

		varsets = self.obs_props["Set"].dropna().unique()

		for varset in varsets:
			g.add(
				(
					URIRef(f"""{varset}"""), 
					RDF.type, 
					URIRef("https://w3id.org/iadopt/ont/VariableSet")
				)
			)

class ConstraintConverter():

	def __init__(self, constraints:pd.DataFrame):
		try:
			if not constraints.columns == ("Name","InDbName","ConstraintOf","AltURI","DataType"):
				self.constraints = constraints
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_constraints.tsv: {e}")

	@property
	def constraints(self):
		return self._constraints

	@constraints.setter
	def constraints(self, value):
		self._constraints = value

	def constraints_triples(self, g:Graph):
		
		for index, row in self.constraints.iterrows():
			g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef(row["AltURI"])
				)
			)
			g.add(
				(
					URIRef(row["InDbName"]),
					URIRef("iop:constrains"),
					URIRef(row["ConstraintOf"])
				)
			)

class ASVConverter():

	# Wait for Marie's code

	def __init__(self, biomfile):
		self.biomfile = biomfile
