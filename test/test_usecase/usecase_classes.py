#!/usr/bin/env python

from genecodata.data_parser.tabular_data_parsers import TableParser, ExcelParser

import pandas as pd

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

import logger

class DPUseCaseObservationConverter():

	def __init__(self, table:ExcelParser, temporalities:pd.DataFrame):
		self.table = table # 2 df : data + metadata
		self.temporalities = temporalities

	def observations_triples(self, g:Graph):

		temporality = f"""{self.table.metadata["Sampling campaign"]}-{self.table.metadata["Sampling season"]}"""
		temporality_rdf = self.temporalities.loc[temporality, "InDbName"]

		# TODO find an alternative to pandas
		for index, row in self.data.data.iterrows():
			for var in row:
				obs_id = f"""Obs-{index}-{var}-{temporality}"""

				g.add((URIRef(f":{obs_id}"), RDF.type, URIRef("http://www.w3.org/ns/sosa/Observation")))
				g.add((URIRef(f":{obs_id}"), URIRef("http://www.w3.org/ns/sosa/phenomenonTime"), URIRef(temporality_rdf)))
				g.add((URIRef(f":{obs_id}"), URIRef("http://www.w3.org/ns/sosa/madeBySensor"), URIRef(self.table.data.loc[index, row["OPERATOR"]])))
				g.add((URIRef(f":{obs_id}"), URIRef("http://www.w3.org/ns/sosa/resultTime"), URIRef(self.table.data.loc[index, row["DATE"]])))
				g.add((URIRef(f":{obs_id}"), URIRef("http://www.w3.org/ns/sosa/observedProperty"), URIRef(var)))
				g.add((URIRef(f":{obs_id}"), URIRef("http://www.w3.org/ns/sosa/hasFeatureOfInterest"), URIRef(index)))
				g.add((URIRef(f":{obs_id}"), URIRef("http://www.w3.org/ns/sosa/hasSimpleResult"), URIRef(row[var])))

class DPUseCaseTemporalityConverter():

	def __init__(self, temporalities:pd.DataFrame):
		"""
		Parameters:
			temporalities (pd.DataFrame) : read from a 3 columns table : "Name": the temporality name in the user data, "InDbName" the name to use in the integrated RDF data, if different, "Nesting": if applicable, the InDbName of the temporality in which it is included) 
		"""
		try:
			if not temporalities.columns == ("Name","InDbName","Nesting"):
				self.temporalities = temporalities
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_temporalities.tsv: {e}")

	def temporalities_triples(self, g:Graph):
		"""
		Sets up temporalities that will be linked to sosa:Observations according to the user config file 

		Parameters:
			g (rdflib:Graph) : an existing RDF graph
		"""

		for tempo in self.temporalities.index:
			g.add(
				(
					URIRef(self.temporalities.loc[tempo, "InDbName"]), 
					RDF.type, 
					URIRef("https://www.w3.org/2006/time#TimeInterval")
				)
			)

			if not pd.isna(self.temporalities.loc[tempo, "Nesting"]):
				g.add(
					(
						URIRef(self.temporalities.loc[tempo, "InDbName"]), 
		   				URIRef("https://www.w3.org/2006/time#intervalWithin"), 
						URIRef(self.temporalities.loc[tempo, "Nesting"])
					)
				)
				g.add(
					(
						URIRef(self.temporalities.loc[tempo, "Nesting"]), 
		   				URIRef("https://www.w3.org/2006/time#intervalContains"), 
		   				URIRef(self.temporalities.loc[tempo, "InDbName"])
					)
				)

class DPUseCaseFeatureOfInterestCategorizer():

	def __init__(self, locations:ExcelParser):
		self.locations = locations

	def region_triples(self, g:Graph):

		for region in self.locations["REGION"].unique():
			g.add((URIRef(region),RDF.type, URIRef("https://schema.org/Thing/Place")))

	def locations_triples(self, g:Graph):

		# TODO check if correct envo and agro URIs
		for index in self.locations.index:
			# Field
			g.add((URIRef(index), RDF.type, URIRef("http://www.w3.org/ns/sosa/FeatureOfInterest")))
			g.add((URIRef(index), RDF.type, URIRef("https://schema.org/Thing/Place")))
			g.add((URIRef(index), RDF.type, URIRef("http://purl.obolibrary.org/obo/envo.owl#00000114")))
			g.add((URIRef(index), URIRef("https://schema.org/Thing/containedInPlace"), URIRef(self.locations.loc[index, "REGION"])))

			# Plots
			for idp in ("PA", "PB", "PC", "PD", "P1", "P2", "P3", "P4"):
				g.add((URIRef(f"{index}-{idp}"), RDF.type, URIRef("http://www.w3.org/ns/sosa/FeatureOfInterest")))
				g.add((URIRef(f"{index}-{idp}"), RDF.type, URIRef("https://schema.org/Thing/Place")))
				g.add((URIRef(f"{index}-{idp}"), RDF.type, URIRef("http://purl.obolibrary.org/obo/AGRO_00000301")))
				g.add((URIRef(f"{index}-{idp}"), URIRef("https://schema.org/Thing/containedInPlace"), URIRef(index)))

class DPUseCaseSensorConverter():

	def __init__(self, sensors:pd.DataFrame):
		try:
			if not sensors.columns == ("Name","InDbName","Type"):
				self.sensors = sensors
		except AssertionError as e:
			logger.error(f"Error : please check colnames of config_sensors.tsv: {e}")

	def sensors_triples(self, g:Graph):

		for sensor, row in self.sensors.iterrows():
			g.add(
				(
					URIRef(row["InDbName"]),
					RDF.type,
					URIRef(row["Type"])
				)
			)