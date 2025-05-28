#!/usr/bin/env python

from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, XSD, TIME, FOAF
from abc import ABC, abstractmethod

import pandas as pd
import logger

from tqdm import tqdm

# OPTI : maybe read_csv within classes rather than pd.DataFrame in constructor

template = {
	("les noms de colonnes de observations_templates.tsv"): "observations",
	("les noms de colonnes de config_observable_properties.tsv"): "observable_properties"
}


class GraphManager():

	def __init__(self, prefixes):
		self.prefixes = prefixes
		self.g = Graph()
		self.namespaces = {k:Namespace(v) for k,v in prefixes.items()}

	@property
	def prefixes(self):
		return self._prefixes

	@prefixes.setter
	def prefixes(self, value):
		self._prefixes = value

	def bind_prefixes(self):
		"""Parse all the prefixes and bind them to the graph g"""

		# for k, v in self.prefixes.items():
		# 	ns = Namespace(str(v))
		# 	self.g.bind(str(k), ns)

		for k, v in self.namespaces.items():
			self.g.bind(k, v)

# class DataConverter(ABC):

# 	def __init__(self, data:pd.DataFrame, expected_cols:tuple):
# 		try:
# 			if data.index.name == "Name" and tuple(data.columns) == expected_cols:
# 				self.constraints = data
# 		except AssertionError as e:
# 			logger.error(f"Error : please check colnames of {template[expected_cols]}.tsv: {e}")

# 	@property
# 	def data(self):
# 		return self._data

# 	@data.setter
# 	def data(self, value):
# 		self._data = value

# 	@property
# 	def expected_cols(self):
# 		return self._expected_cols

# 	@expected_cols.setter
# 	def expected_cols(self, value):
# 		self._expected_cols = value

# 	@abstractmethod
# 	def build_triples(self, g):
# 		pass


class TemporalityConverter():

	def __init__(self, table:pd.DataFrame):
		"""
		Parameters:
			table (pd.DataFrame) : read from a 3 columns table : "Name": the temporality name in the user data, "InDbName" the name to use in the integrated RDF data, if different, "Nesting": if applicable, the InDbName of the temporality in which it is included) 
		"""
		try:
			if table.index.name == "Name" and tuple(table.columns) == ("InDbName","Nesting"):
				self.table = table
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_temporalities.tsv: {e}")

	def build_triples(self, gm:GraphManager):
		"""
		Sets up temporalities that will be linked to sosa:Observations according to the user config file 

		Parameters:
			g (rdflib:Graph) : an existing RDF graph
		"""

		for tempo in tqdm(self.table.index, total=self.table.shape[0]):
			gm.g.add(
				(
					URIRef(self.table.loc[tempo, "InDbName"]),
					RDF.type, 
					# URIRef("TimeInterval", gm.namespaces["time"])
					TIME.Interval
				)
			)

			if not pd.isna(self.table.loc[tempo, "Nesting"]):
				gm.g.add(
					(
						URIRef(self.table.loc[tempo, "InDbName"]), 
						#URIRef("intervalWithin", gm.namespaces["time"]),
						URIRef(TIME.intervalDuring),
						URIRef(self.table.loc[tempo, "Nesting"])
					)
				)
				gm.g.add(
					(
						URIRef(self.table.loc[tempo, "Nesting"]),
						# URIRef("intervalContains", gm.namespaces["time"]),
						URIRef(TIME.intervalContains),
						URIRef(self.table.loc[tempo, "InDbName"])
					)
				)

class SensorConverter():

	def __init__(self, table:pd.DataFrame):
		try:
			if table.index.name == "Name" and tuple(table.columns) == ("InDbName","Type"):
				self.table = table
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_sensors.tsv: {e}")

	def build_triples(self, gm:GraphManager):

		for sensor, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):
			base, value = row["Type"].split(":")
			gm.g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,					
					URIRef(value, gm.namespaces["foaf"])
				)
			)

class ObservablePropertiesConverter():
	"""Convert Config data loaded in a TableParser object into RDF triples"""

	def __init__(self, table:pd.DataFrame):
		try:
			if table.index.name == "Name" and tuple(table.columns) == ("InDbName","AltURI","Set", "Unit","DataType"):
				self.table = table
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_variables.tsv: {e}")

	@property
	def table(self):
		return self._table

	@table.setter
	def table(self, value):
		self._table = value

	def build_variables_triples(self, gm:GraphManager):
		"""Parse config table and set up triples of sosa:ObservableProperties"""

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):
			gm.g.add(
				(					
					URIRef(f"""{row["InDbName"]}"""),					
					RDF.type, 
					URIRef("Property", gm.namespaces["sosa"])
				)
			)
			gm.g.add(
				(					
					URIRef(f"""{row["InDbName"]}"""),
					RDF.type,
					URIRef("Variable", gm.namespaces["iop"])
				)
			)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					base, value = uri.split(":")

					gm.g.add(
						(							
							URIRef(f"""{row["InDbName"]}"""),
							RDF.type,
							URIRef(value, gm.namespaces[base])
						)
					)

			if not pd.isna(row["Set"]):
				gm.g.add(
					(
						URIRef(f"""{row["Set"]}"""), 
						URIRef("hasMember", gm.namespaces["iop"]),
						URIRef(f"""{row["InDbName"]}""")						
					)
				)
	
	def build_variables_sets_triples(self, gm:GraphManager):
		"""Parse config file and set up triples of variable sets"""

		varsets = self.table["Set"].dropna().unique()

		for varset in varsets:
			gm.g.add(
				(
					URIRef(f"""{varset}"""), 
					RDF.type, 
					URIRef("VariableSet", gm.namespaces["iop"])
				)
			)

class ConstraintConverter():

	def __init__(self, table:pd.DataFrame):
		try:
			if table.index.name == "Name" and tuple(table.columns) == ("InDbName","ConstraintOf","AltURI","DataType"):
				self.table = table
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_constraints.tsv: {e}")

	@property
	def table(self):
		return self._table

	@table.setter
	def table(self, value):
		self._table = value

	def build_triples(self, gm:GraphManager):
		
		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):
			gm.g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef("Constraint", gm.namespaces["iop"])
				)
			)

			gm.g.add(
				(
					URIRef(row["InDbName"]),
					URIRef("constrains", gm.namespaces["iop"]),
					URIRef(row["ConstraintOf"])
				)
			)

			if not pd.isna(row["AltURI"]):
				base, value = row["AltURI"].split(":")
				gm.g.add(
					(
						URIRef(row["InDbName"]),
						RDF.type,
						URIRef(value, gm.namespaces[base])
					)
				)

class FeatureOfInterestConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def build_triples(self, gm:GraphManager):

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			gm.g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef("FeatureOfInterest", gm.namespaces["sosa"])
				)
			)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					base, value = uri.split(":")
					gm.g.add(
						(
							URIRef(row["InDbName"]),
							RDF.type,
							URIRef(value, gm.namespaces[base])
						)
					)

			if not pd.isna(row["thing:locatedIn"]):
				gm.g.add(
					(
						URIRef(row["InDbName"]),
						URIRef("locatedIn", gm.namespaces["thing"]),
						URIRef(row["thing:locatedIn"])
					)
				)

class SampleConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def build_triples(self, gm:GraphManager):
		
		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):
			gm.g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef("Sample", gm.namespaces["sosa"])
				)
			)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					base, value = uri.split(":")
					gm.g.add(
						(
							URIRef(row["InDbName"]),
							RDF.type,
							URIRef(value, gm.namespaces[base])
						)
					)

			gm.g.add(
				(
					URIRef(row["InDbName"]),
					URIRef("isSampleOf", gm.namespaces["sosa"]),
					URIRef(row["sosa:isSampleOf"])
				)
			)

class ASVConverter():

	# Wait for Marie's code

	def __init__(self, biomfile):
		self.biomfile = biomfile

class ObservationConverter():

	def __init__(self, table:pd.DataFrame):
			self.table = table

	def build_triples(self, gm:GraphManager):

		colset = list(self.table.columns)
		colset.remove("sosa:hasUltimateFeatureOfInterest")
		colset.remove("sosa:hasResult")
		colset.remove("unit")
		colset.remove("datatype")

		xsd = {
			"integer": XSD.integer,
			"float": XSD.float,
			"boolean": XSD.boolean,
			"string": XSD.string}

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):
			gm.g.add(
				(
					URIRef(index),
					RDF.type,
					URIRef("Observation", gm.namespaces["sosa"])
				)
			)
			# Common to every triplet			
			for col in colset:
				base, value = col.split(":")
				if not pd.isna(row[col]):		
					gm.g.add(
						(
							URIRef(index), 
							URIRef(value, gm.namespaces[base]),
							URIRef(row[col])
						)
					)

			# if there is a sosa:hasUltimateFeatureOfInterest
			if not pd.isna(row["sosa:hasUltimateFeatureOfInterest"]):
				gm.g.add(
					(
						URIRef(index), 
						URIRef(value="hasUltimateFeatureOfInterest", base=gm.namespaces["sosa"]),
						URIRef(row["sosa:hasUltimateFeatureOfInterest"])
					)
				)
			
			# Differentiate sosa:hasResult and sosa:hasSimpleresult
			#if  not pd.isna(row["unit"]):
			if  row["unit"] != "No unit":
				bn = BNode()
				gm.g.add(
					(
						URIRef(index), 
						URIRef(value="hasResult", base=gm.namespaces["sosa"]), 
						bn
					)
				)
				gm.g.add(
					(
						bn, 
						RDF.type, 
						URIRef(value="QuantityValue", base=gm.namespaces["qudt"])
					)
				)

				base, value = self.table.loc[index, "unit"].split(":") 
				gm.g.add(
					(
						bn, 
						URIRef(value="hasUnit", base=gm.namespaces["qudt"]), 
						URIRef(value=value, base=base)
					)
				)
				_, value = self.table.loc[index, "datatype"].split(":")
				gm.g.add(
					(
						bn, 
						URIRef(value="value", base=gm.namespaces["qudt"]), 
						Literal(row["sosa:hasResult"])#, datatype=xsd[value]) # Investigate : datatype might raise warnings / errors
					)
				)
			
			else:
				# Use the alternate Result property if no unit
				_, value = row["datatype"].split(":")

				gm.g.add(
					(
						URIRef(index), 
						URIRef(value="hasSimpleResult", base=gm.namespaces["sosa"]), 
						Literal(row["sosa:hasResult"])#, datatype=xsd[value])
					)
				)

dtypes = {
	"float": XSD.float,
	"integer": XSD.integer,
	"bool": XSD.boolean,
	"str": XSD.string }