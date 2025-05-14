#!/usr/bin/env python

from genecodata.data_parser.tabular_data_parsers import TableParser, ExcelParser

import pandas as pd

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

import logger

"""
Classes specific to DeepImpact data : convert deepimpact tables to the expected templates.
Input is a already configured graph which includes all instances of :
	- sosa:FeatureOfInterest
	- sosa:ObservableProperty / iop:Variable
	- iop:Constraint
	- iop:Property
"""

COLUMN_NAMES = ["sosa:Observation",
				"sosa:observedProperty",
				"sosa:hasFeatureOfInterest",
				"sosa:hasUltimateFeatureOfInterest",
				"sosa:hasResult",
				"sosa:resultTime",
				"sosa:phenomenonTime",
				"sosa:madeBySensor",
				"unit",
				"datatype"]

class DPUseCaseBiomassConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, plot = index.split()

			for col in columns:
				new_row = {k:None for k in COLUMN_NAMES}
				new_row["sosa:Observation"] = f"""Obs-biomass-{field}-{year}-{counter}"""
				new_row["sosa:observedProperty"] = col
				new_row["sosa:hasFeatureOfInterest"] = "-".join(field, plot)
				new_row["sosa:hasUltimateFeatureOfInterest"] = field
				new_row["sosa:phenomenonTime"] = year
				new_row["hasResult"] = row[col]
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] =row["OPERATOR"]
				new_row["unit"] = config_variables.loc[col, "Unit"]
				new_row["datatype"] = config_variables.loc[col, "DataType"]

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile)

class DPUseCaseYieldsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, plot = index.split()

			for col in columns:
				new_row = {k:None for k in COLUMN_NAMES}
				new_row["sosa:Observation"] = f"""Obs-yield-{field}-{year}-{counter}"""
				new_row["sosa:observedProperty"] = col
				new_row["sosa:hasFeatureOfInterest"] = "-".join(field, plot)
				new_row["sosa:hasUltimateFeatureOfInterest"] = field
				new_row["sosa:phenomenonTime"] = year
				new_row["hasResult"] = row[col]
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] =row["OPERATOR"]
				new_row["unit"] = config_variables.loc[col, "Unit"]
				new_row["datatype"] = config_variables.loc[col, "DataType"]

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile)

class DPUseCaseNirsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, plot = index.split()

			for col in columns:
				new_row = {k:None for k in COLUMN_NAMES}
				new_row["sosa:Observation"] = f"""Obs-nirs-{field}-{year}-{counter}"""
				new_row["sosa:observedProperty"] = col
				new_row["sosa:hasFeatureOfInterest"] = "-".join(field, plot)
				new_row["sosa:hasUltimateFeatureOfInterest"] = field
				new_row["sosa:phenomenonTime"] = year
				new_row["hasResult"] = row[col]
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] =row["OPERATOR"]
				new_row["unit"] = config_variables.loc[col, "Unit"]
				new_row["datatype"] = config_variables.loc[col, "DataType"]

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile)

class DPUseCaseSoiBiochemistryConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, season = index.split()

			for col in columns:
				new_row = {k:None for k in COLUMN_NAMES}
				new_row["sosa:Observation"] = f"""Obs-Soil-{field}-{"".join(year, season)}-{counter}"""
				new_row["sosa:observedProperty"] = col
				new_row["sosa:hasFeatureOfInterest"] = field
				new_row["sosa:hasUltimateFeatureOfInterest"] = ""
				new_row["sosa:phenomenonTime"] = "".join(year, season)
				new_row["hasResult"] = row[col]
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] =row["OPERATOR"]
				new_row["unit"] = config_variables.loc[col, "Unit"]
				new_row["datatype"] = config_variables.loc[col, "DataType"]

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile)


class DPUseCaseWeedsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, season, plot = index.split()

			new_row = {k:None for k in COLUMN_NAMES}
			new_row["sosa:Observation"] = f"""Obs-Weed-{field}-{row["WEED_SPECIES"]}-{"".join(year, season)}-{counter}"""
			new_row["sosa:observedProperty"] = f"""Density-{row["WEED_SPECIES"]}-Stage-{row["PHENOLOGY_STAGE"]}"""
			new_row["sosa:hasFeatureOfInterest"] = "-".join(field, plot)
			new_row["sosa:hasUltimateFeatureOfInterest"] = field
			new_row["sosa:phenomenonTime"] = "".join(year, season)
			new_row["hasResult"] = row["ABONDANCE"]
			new_row["sosa:resultTime"] = row["DATE"]
			new_row["sosa:madeBySensor"] = row["OPERATOR"]
			new_row["unit"] = config_variables.loc["ABONDANCE", "Unit"]
			new_row["datatype"] = config_variables.loc["DENSITY_CLASS", "DataType"]

			new_row["iop:Entity"] = row["WEED_SPECIES"]
			new_row["iop:Property"] = "Density"
			new_row["iop:Constraint"] = row["PHENOLOGY_STAGE"]

			out_table.loc[len(out_table)] = new_row
			counter += 1

		out_table.to_csv(outfile)

class DPUseCaseBioagressorsConverter():

	def __init__(self, table_general:pd.DataFrame, table_field:pd.DataFrame, table_lab:pd.DataFrame):
		self.table_general = table_general
		self.table_field = table_field
		self.table_lab = table_lab

	def convert_general_table(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		# columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, season, plot = index.split()

			for col in ["PEST_DENSITY", "GENERAL_STATE"]:
				new_row = {k:None for k in COLUMN_NAMES}
				new_row["sosa:Observation"] = f"""Obs-fieldState-{field}-{"".join(year, season)}-{counter}"""
				new_row["sosa:observedProperty"] = col
				new_row["sosa:hasFeatureOfInterest"] = "-".join(field, plot)
				new_row["sosa:hasUltimateFeatureOfInterest"] = field
				new_row["sosa:phenomenonTime"] = "".join(year, season)
				new_row["hasResult"] = row[col]
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] =row["OPERATOR"]
				new_row["unit"] = config_variables.loc[col, "Unit"]
				new_row["datatype"] = config_variables.loc[col, "DataType"]

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile)

	def convert_detail_table(self, config_variables:pd.DataFrame, sampling:str, outfile:str):

		values = {"FieldSampled", "LabSampled"}
		if sampling not in values:
			raise ValueError("'sampling' must be one of %r" % values)

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["PLANT", "DATE", "OPERATOR"]]

		counter = 1

		for index, row in self.table.iterrows():

			field, _, year, season, plot = index.split()

			for col in columns:
				new_row = {k:None for k in COLUMN_NAMES}
				new_row["sosa:Observation"] = f"""Obs-BioAgr-{sampling}-{field}-{plot}-{row["PLANT"]}-{"".join(year, season)}-{counter}"""
				new_row["sosa:observedProperty"] = "Presence-{col}-on-{sampling}-plants"
				new_row["sosa:hasFeatureOfInterest"] = "-".join(field, plot)
				new_row["sosa:hasUltimateFeatureOfInterest"] = field
				new_row["sosa:phenomenonTime"] = "".join(year, season)
				new_row["hasResult"] = row[col]
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] =row["OPERATOR"]
				new_row["unit"] = config_variables.loc[col, "Unit"]
				new_row["datatype"] = config_variables.loc[col, "DataType"]

				new_row["iop:Entity"] = col
				new_row["iop:Property"] = "SpeciesPresence"
				new_row["iop:Constraint"] = sampling

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile)


class DPUseCaseFeatureOfInterestConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, table:pd.DataFrame):

		regions = self.table["REGION".unique()]
		regions = {k:k[0]+k[1:].lower() for k in regions}

		out_table = pd.DataFrame(columns=["Name", "InDbName", "InDbType", "AltURI", "thing:locatedIn"])

		for k, v in regions.keys():
			new_row = {k:"" for k in out_table.columns}

			new_row["Name"] = k
			new_row["InDbName"] = v
			new_row["InDbType"] = "Region""
			new_row["AltURI"] = "thing:Place"

			out_table.loc[len(out_table)] = new_row

		for index, row in self.table.iterrows():
			new_row = {k:"" for k in out_table.columns}

			# Sampling Fields
			new_row["Name"] = index
			new_row["InDbName"] = index.split()[0]
			new_row["InDbType"] = "SampledField""
			new_row["AltURI"] = "thing:Place,envo:00000114"
			new_row["thing:locatedIn"] = regions[row["REGION"]]

			out_table.loc[len(out_table)] = new_row


	# def region_triples(self, g:Graph):

	# 	for region in self.locations["REGION"].unique():
	# 		g.add((URIRef(region),RDF.type, URIRef("https://schema.org/Thing/Place")))

	# def locations_triples(self, g:Graph):

	# 	# TODO check if correct envo and agro URIs
	# 	for index in self.locations.index:
	# 		# Field
	# 		g.add((URIRef(index), RDF.type, URIRef("http://www.w3.org/ns/sosa/FeatureOfInterest")))
	# 		g.add((URIRef(index), RDF.type, URIRef("https://schema.org/Thing/Place")))
	# 		g.add((URIRef(index), RDF.type, URIRef("http://purl.obolibrary.org/obo/envo.owl#00000114")))
	# 		g.add((URIRef(index), URIRef("https://schema.org/Thing/containedInPlace"), URIRef(self.locations.loc[index, "REGION"])))

	# 		# Plots
	# 		for idp in ("PA", "PB", "PC", "PD", "P1", "P2", "P3", "P4"):
	# 			g.add((URIRef(f"{index}-{idp}"), RDF.type, URIRef("http://www.w3.org/ns/sosa/FeatureOfInterest")))
	# 			g.add((URIRef(f"{index}-{idp}"), RDF.type, URIRef("https://schema.org/Thing/Place")))
	# 			g.add((URIRef(f"{index}-{idp}"), RDF.type, URIRef("http://purl.obolibrary.org/obo/AGRO_00000301")))
	# 			g.add((URIRef(f"{index}-{idp}"), URIRef("https://schema.org/Thing/containedInPlace"), URIRef(index)))

