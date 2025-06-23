#!/usr/bin/env python

import pandas as pd

class AskomicsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def rename_and_write(self, askomics_colnames:dict, outfile:str):

		self.table.rename(
			{
				col:askomics_colnames[col] for col in self.table.columns if col in askomics_colnames.keys()
			}
		)

		self.table.to_csv(outfile, index=False)

OBSERVATIONS_ASKOMICS_COLNAMES = {
	"sosa:Observation": "Observation",
	"sosa:observedProperty": "observedProperty@Variable",
	"sosa:hasFeatureOfInterest": "hasFeatureOfInterest@SampledField",
	"sosa:hasUltimateFeatureOfInterest": "",
	"sosa:hasResult": "Value",
	"sosa:resultTime": "Date",
	"sosa:phenomenonTime": "phenomenonTime@TimeInterval",
	"sosa:madeBySensor": "madeBy@Sensor",
	"unit": "Unit"
}

VARIABLES_ASKOMICS_COLNAMES = {

}

VARIABLESSETS_ASKOMICS_COLNAMES = {

}

CONSTRAINTS_ASKOMICS_COLNAMES = {

}

TEMPORALITIES_ASKOMICS_COLNAMES = {

}

SENSORS_ASKOMICS_COLNAMES = {

}

def main():

	variables = pd.read_csv("")
	variables_sets = pd.read_csv("")
	constraints = pd.read_csv("")
	temporalities = pd.read_csv("")
	sensors = pd.read_csv("")

# class AskomicsObservationConverter():

# 	def __init__(self, table:pd.DataFrame):
# 		self.table = table

# 	def rename_and_write(self):

# 		self.table.rename(
# 			{
# 				"sosa:Observation": "Observation",
# 				"sosa:observedProperty": "observedProperty@Variable",
# 				"sosa:hasFeatureOfInterest": "hasFeatureOfInterest@SampledField",
# 				"sosa:hasUltimateFeatureOfInterest": "",
# 				"sosa:hasResult": "Value",
# 				"sosa:resultTime": "Date",
# 				"sosa:phenomenonTime": "phenomenonTime@TimeInterval",
# 				"sosa:madeBySensor": "madeBy@Sensor",
# 				"unit": "Unit"
# 			}
# 		)

class AskomicsVariableConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def rename(self):

		self.table.rename(
			{
				"InDbName": "MeasuredProperty",
				"AltURI": "uriInOtherOntologies",
				"Set": "partOf@VariableSet",
				"Unit": "Unit"
			}
		)
		
class AskomicsConstraintConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def rename_and_write(self, outfile):

		self.table.rename(
			{
				"ConstraintOf": "ConstraintOf@Variable",
				"AltURI": "uriInOtherOntologies",
				"Set": "partOf@VariableSet",
				"Unit": "Unit"
			}
		)

		self.table.to_csv(outfile, index=False)

class AskomicsFoIConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def rename(self):

		self.table.rename(
			{
				"": "",
				"": "",
				"": "",	
			}
		)

class AskomicsTempoConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def rename(self):

		self.table.rename(
			{
				"": "",
				"": "",
				"": "",	
			}
		)

class AskomicsSensorConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def rename(self):

		self.table.rename(
			{
				"": "",
				"": "",
				"": "",	
			}
		)