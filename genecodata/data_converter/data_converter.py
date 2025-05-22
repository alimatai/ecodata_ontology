#!/usr/bin/env python

from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, XSD
from abc import ABC, abstractmethod

import pandas as pd
import logger

from tqdm import tqdm

template = {
	("les noms de colonnes de observations_templates.tsv"): "observations",
	("les noms de colonnes de config_observable_properties.tsv"): "observable_properties"
}

class GraphManager():

	def __init__(self, prefixes_dfpath):
		try:
			tmp = pd.read_csv(prefixes_dfpath, index_col=0, header=0, sep="\t")
			if tuple(tmp.columns) == ("Prefix","URI"):
				self.prefixes = tmp.to_dict()
				self.g = Graph()
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_prefixes.tsv: {e}")

	@property
	def prefixes(self):
		return self._prefixes

	@prefixes.setter
	def prefixes(self, value):
		self._prefixes = value

	def bind_prefixes(self):
		"""Parse all the prefixes and bind them to the graph g"""

		for k, v in self.prefixes.items():
			ns = Namespace(v)
			self.g.bind(k, ns)


class DataConverter(ABC):

	def __init__(self, data:pd.DataFrame, expected_cols:tuple):
		try:
			if tuple(data.columns) == expected_cols:
				self.constraints = data
		except AssertionError as e:
			logger.error(f"Error : please check colnames of {template[expected_cols]}.tsv: {e}")

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		self._data = value

	@property
	def expected_cols(self):
		return self._expected_cols

	@expected_cols.setter
	def expected_cols(self, value):
		self._expected_cols = value

	@abstractmethod
	def build_triples(self, g):
		pass

# class PrefixesBinder():
# 	"""
# 	Sets prefixes and namespaces of a graph. Must be used first, before eveything else
# 	"""

# 	def __init__(self, project_prefixes:pd.DataFrame):
# 		try:
# 			if tuple(project_prefixes.columns) == ("Prefix","URI"):
# 				self.project_prefixes = project_prefixes
# 		except AssertionError as e:
# 			logger.error(f"Error : please check colnames of config_prefixes.tsv: {e}")

# 	@property
# 	def project_prefixes(self):
# 		return self._project_prefixes

# 	@project_prefixes.setter
# 	def project_prefixes(self, value):
# 		self._project_prefixes = value

# 	def bind_prefixes(self, g:Graph):
# 		"""Parse all the prefixes and bind them to the graph g"""

# 		for index, row in self.project_prefixes.iterrows():
# 			ns = Namespace(row["URI"])
# 			g.bind(index, ns)

class TemporalityConverter():

	def __init__(self, table:pd.DataFrame):
		"""
		Parameters:
			table (pd.DataFrame) : read from a 3 columns table : "Name": the temporality name in the user data, "InDbName" the name to use in the integrated RDF data, if different, "Nesting": if applicable, the InDbName of the temporality in which it is included) 
		"""
		try:
			if not table.columns == ("Name","InDbName","Nesting"):
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
					URIRef("https://www.w3.org/2006/time#TimeInterval")
				)
			)

			if not pd.isna(self.table.loc[tempo, "Nesting"]):
				gm.g.add(
					(
						URIRef(self.table.loc[tempo, "InDbName"]), 
						URIRef("https://www.w3.org/2006/time#intervalWithin"), 
						URIRef(self.table.loc[tempo, "Nesting"])
					)
				)
				gm.g.add(
					(
						URIRef(self.table.loc[tempo, "Nesting"]), 
						URIRef("https://www.w3.org/2006/time#intervalContains"), 
						URIRef(self.table.loc[tempo, "InDbName"])
					)
				)

class SensorConverter():

	def __init__(self, table:pd.DataFrame):
		try:
			if not table.columns == ("Name","InDbName","Type"):
				self.table = table
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_sensors.tsv: {e}")

	def build_triples(self, gm:GraphManager):

		for sensor, row in tqdm(self.table.index, total=self.table.shape[0]):
			base, value = row["Type"].split()
			gm.g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef(value=value, base=gm.prefixes[base]) # ex: foaf:Person TODO check if base has to be str or rdflib.Namespace
				)
			)

class ObservablePropertiesConverter():
	"""Convert Config data loaded in a TableParser object into RDF triples"""

	def __init__(self, table:pd.DataFrame):
		try:
			if tuple(table.columns) == ("Name","InDbName","AltURI","Set", "Unit","DataType"):
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

		for _, row in tqdm(self.table.index, total=self.table.shape[0]):
			gm.g.add(
				(					
					URIRef(f"""{row["InDbName"]}"""),					
					RDF.type, 
					URIRef("http://www.w3.org/ns/sosa/Observableproperty")
				)
			)
			gm.g.add(
				(					
					URIRef(f"""{row["InDbName"]}"""),
					RDF.type,
					URIRef("https://w3id.org/iadopt/ont/Variable")
				)
			)

			if not pd.isna(row["AltURI"]):
				for uri in row["AltURI"].split(","):
					base, value = uri.split()
					gm.g.add(
						(							
							URIRef(f"""{row["InDbName"]}"""),
							RDF.type,
							URIRef(value=value, base=gm.prefixes[base])
						)
					)

			if not pd.isna(row["Set"]):
				gm.g.add(
					(
						URIRef(f"""{row["Set"]}"""), 
						URIRef("https://w3id.org/iadopt/ont/hasMember/"),
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
					URIRef("https://w3id.org/iadopt/ont/VariableSet")
				)
			)

class ConstraintConverter():

	def __init__(self, table:pd.DataFrame):
		try:
			if tuple(table.columns) == ("Name","InDbName","ConstraintOf","AltURI","DataType"):
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
		
		for _, row in self.table.iterrows():
			base, value = row["AltURI"].split()
			gm.g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef(value=value, base=gm.prefixes[base])
				)
			)
			gm.g.add(
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

# class ObservationConverter(DataConverter):

# 	def __init__(self, table:pd.DataFrame, expected_cols:tuple):
# 		super().__init__(self, table, expected_cols)

# 	def build_triples(self, gm:GraphManager):

# 		colset = list(self.table.columns)
# 		colset.remove("sosa:hasultimateFeatureOfinterest", "sosa:hasResult", "unit", "datatype")

# 		# Loop 1 : no particular cases
# 		for index, row in self.table.iterrows():
# 			gm.g.add((URIRef(index), RDF.type, URIRef(value="Observation", base=gm.prefixes["sosa"])))

# 			for col in row:
# 				if col in colset:
# 					base, value = col.split()
# 					gm.g.add(
# 						(
# 							URIRef(index), 
# 							URIRef(value=value, base=gm.prefixes["sosa"]), 
# 							URIRef(row[col])
# 						)
# 					)

# 		# Loop 2 : particular cases
# 		# TODO : skip if result is boolean = False (0)
# 		for index in self.table.index:

# 			if not pd.isna(self.table.loc[index, "sosa:hasultimateFeatureOfinterest"]):
# 				gm.g.add(
# 					(
# 						URIRef(index), 
# 			  			URIRef(value="hasUltimateFeatureOfinterest", base=gm.prefixes["sosa"]), 
# 						URIRef(self.table.loc[index, "sosa:hasUltimateFeatureOfinterest"])
# 					)
# 				)
			
# 			if not pd.isna(self.table.loc[index, "unit"]):
# 				bn = BNode()
# 				gm.g.add(
# 					(
# 						URIRef(index), 
# 						URIRef(value="hasResult", base=gm.prefixes["sosa"]), 
# 						bn
# 					)
# 				)
# 				gm.g.add(
# 					(
# 						bn, 
# 						RDF.type, 
# 						URIRef(value="QuantityValue", base=gm.prefixes["qudt"])))
# 				base, value = self.table.loc[index, "unit"].split() 
# 				gm.g.add(
# 					(
# 						bn, 
# 						URIRef(value="hasUnit", base=gm.prefixes["qudt"]), 
# 						URIRef(value=value, base=base)
# 					)
# 				)
# 				_, value = self.table.loc[index, "datatype"].split()			
# 				gm.g.add(
# 					(
# 						bn, 
# 						URIRef(value="value", base=gm.prefixes["qudt"]), 
# 						Literal(self.table.loc[index, "sosa:hasResult"], datatype=dtypes[value])
# 					)
# 				) # TODO Fix dtype
			
# 			else:
# 				# Use the alternate Result property if no unit
# 				_, value = self.table.loc[index, "datatype"].split()
# 				gm.g.add(
# 					(
# 						URIRef(index), 
# 						URIRef(value="hasSimpleResult", base=gm.prefixes["sosa"]), 
# 						Literal(self.table.loc[index, "sosa:hasResult"], datatype=dtypes[value])
# 					)
# 				)

class ObservationConverter(DataConverter):

	def __init__(self, table:pd.DataFrame, expected_cols:tuple):
		super().__init__(self, table, expected_cols)

	def build_triples(self, gm:GraphManager):

		colset = list(self.table.columns)
		colset.remove("sosa:hasultimateFeatureOfinterest", "sosa:hasResult", "unit", "datatype")

		# Loop 1 : no particular cases
		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			# No particular cases
			if pd.isna(self.table.loc[index, "sosa:hasultimateFeatureOfinterest"]):
				gm.g.add(
					(
						URIRef(index), 
						RDF.type, 
						URIRef(value="Observation", base=gm.prefixes["sosa"])
					)
				)

				for col in row:
					if col in colset:
						base, value = col.split()
						gm.g.add(
							(
								URIRef(index), 
								URIRef(value=value, base=gm.prefixes["sosa"]), 
								URIRef(row[col])
							)
						)

			# Particular cases
			# TODO : skip if result is boolean = False (0)
			elif not pd.isna(self.table.loc[index, "sosa:hasultimateFeatureOfinterest"]):
				gm.g.add(
					(
						URIRef(index), 
			  			URIRef(value="hasUltimateFeatureOfinterest", base=gm.prefixes["sosa"]), 
						URIRef(self.table.loc[index, "sosa:hasUltimateFeatureOfinterest"])
					)
				)
			
			# Differentiate sosa:hasResult and sosa:hasSimpleresult
			if not pd.isna(self.table.loc[index, "unit"]):
				bn = BNode()
				gm.g.add(
					(
						URIRef(index), 
						URIRef(value="hasResult", base=gm.prefixes["sosa"]), 
						bn
					)
				)
				gm.g.add(
					(
						bn, 
						RDF.type, 
						URIRef(value="QuantityValue", base=gm.prefixes["qudt"])))
				base, value = self.table.loc[index, "unit"].split() 
				gm.g.add(
					(
						bn, 
						URIRef(value="hasUnit", base=gm.prefixes["qudt"]), 
						URIRef(value=value, base=base)
					)
				)
				_, value = self.table.loc[index, "datatype"].split()			
				gm.g.add(
					(
						bn, 
						URIRef(value="value", base=gm.prefixes["qudt"]), 
						Literal(self.table.loc[index, "sosa:hasResult"], datatype=dtypes[value])
					)
				) # TODO Fix dtype
			
			else:
				# Use the alternate Result property if no unit
				_, value = self.table.loc[index, "datatype"].split()
				gm.g.add(
					(
						URIRef(index), 
						URIRef(value="hasSimpleResult", base=gm.prefixes["sosa"]), 
						Literal(self.table.loc[index, "sosa:hasResult"], datatype=dtypes[value])
					)
				)

dtypes = {
	"float": XSD.float,
	"integer": XSD.integer,
	"bool": XSD.boolean,
	"str": XSD.string }