#!/usr/bin/env python

import pandas as pd
import numpy as np
from tqdm import tqdm

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

ASKO_COLS = ["Observation",
			 	"@observedProperty",
				"@hasFeatureOfInterest",
				"@hasUltimateFeatureOfInterest",
				"hasResult",
				"resultTime",
				"@phenomenonTime",
				"@madeBySensor",
				"unit",
				"datatype"]

class DPUseCaseBiomassConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			field, _, year, plot = index.split("-")

			for col in columns:				
				if not pd.isna(self.table.loc[index, col]):
					new_row = {k:None for k in COLUMN_NAMES}
					new_row["sosa:Observation"] = f"""Obs-biomass-{field}-{counter}"""
					new_row["sosa:observedProperty"] = col
					new_row["sosa:hasFeatureOfInterest"] = "-".join((field, plot))
					new_row["sosa:hasUltimateFeatureOfInterest"] = field
					new_row["sosa:phenomenonTime"] = year
					new_row["sosa:hasResult"] = self.table.loc[index, col] # TODO: very ugly, find better way to parse
					new_row["sosa:resultTime"] = row["DATE"]
					new_row["sosa:madeBySensor"] =row["OPERATOR"]
					new_row["unit"] = config_variables.loc[col, "Unit"]
					new_row["datatype"] = config_variables.loc[col, "DataType"]

					out_table.loc[len(out_table)] = new_row
					counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")

class DPUseCaseYieldsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "DATE_FRESH_SEEDS", "DATE_DRY_SEEDS", "OPERATOR"]]

		counter = 1

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			field, _, year, plot = index.split("-")

			for col in columns:
				if not pd.isna(self.table.loc[index, col]):
					new_row = {k:None for k in COLUMN_NAMES}
					new_row["sosa:Observation"] = f"""Obs-yield-{field}-{counter}"""
					new_row["sosa:observedProperty"] = col
					new_row["sosa:hasFeatureOfInterest"] = "-".join((field, plot))
					new_row["sosa:hasUltimateFeatureOfInterest"] = field
					new_row["sosa:phenomenonTime"] = year
					new_row["sosa:hasResult"] = self.table.loc[index, col] # TODO: very ugly, find better way to parse
					new_row["sosa:resultTime"] = row["DATE"]
					new_row["sosa:madeBySensor"] =row["OPERATOR"]
					new_row["unit"] = config_variables.loc[col, "Unit"]
					new_row["datatype"] = config_variables.loc[col, "DataType"]

					out_table.loc[len(out_table)] = new_row
					counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")

class DPUseCaseNirsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			field, _, year, plot = index.split("-")

			for col in columns:				
				if not pd.isna(self.table.loc[index, col]):
					new_row = {k:None for k in COLUMN_NAMES}
					new_row["sosa:Observation"] = f"""Obs-nirs-{field}-{year}-{counter}"""
					new_row["sosa:observedProperty"] = col
					new_row["sosa:hasFeatureOfInterest"] = "-".join((field, plot))
					new_row["sosa:hasUltimateFeatureOfInterest"] = field
					new_row["sosa:phenomenonTime"] = year
					new_row["sosa:hasResult"] = self.table.loc[index, col] # TODO: very ugly, find better way to parse
					new_row["sosa:resultTime"] = row["DATE"]
					new_row["sosa:madeBySensor"] =row["OPERATOR"]
					new_row["unit"] = config_variables.loc[col, "Unit"]
					new_row["datatype"] = config_variables.loc[col, "DataType"]

					out_table.loc[len(out_table)] = new_row
					counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")

class DPUseCaseSoiBiochemistryConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			field, _, year, season = index.split("-")

			for col in columns:
				if not pd.isna(self.table.loc[index, col]):
					new_row = {k:None for k in COLUMN_NAMES}
					new_row["sosa:Observation"] = f"""Obs-Soil-{field}-{"".join((year, season))}-{counter}"""
					new_row["sosa:observedProperty"] = col
					new_row["sosa:hasFeatureOfInterest"] = field
					new_row["sosa:hasUltimateFeatureOfInterest"] = ""
					new_row["sosa:phenomenonTime"] = "".join((year, season))
					new_row["sosa:hasResult"] = self.table.loc[index, col] # TODO: very ugly, find better way to parse
					new_row["sosa:resultTime"] = np.nan
					new_row["sosa:madeBySensor"] = np.nan
					new_row["unit"] = config_variables.loc[col, "Unit"]
					new_row["datatype"] = config_variables.loc[col, "DataType"]

					out_table.loc[len(out_table)] = new_row
					counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")


class DPUseCaseWeedsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		counter = 1
		colum_names_with_constraints = COLUMN_NAMES + ["iop:Entity", "iop:Property", "iop:Constraint"]
		out_table = pd.DataFrame(columns=colum_names_with_constraints)

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			if not pd.isna(row["DENSITY_CLASS"]):

				field, _, year, season, plot = index.split("-")

				new_row = {k:None for k in colum_names_with_constraints}
				new_row["sosa:Observation"] = f"""Obs-Weed-{field}-{plot}-{row["WEED_SPECIES"]}-{season}-{counter}"""
				new_row["sosa:observedProperty"] = f"""DensityClass-{row["WEED_SPECIES"]}-Stage-{row["PHENOLOGY_STAGE"]}"""
				new_row["sosa:hasFeatureOfInterest"] = "-".join((field, plot))
				new_row["sosa:hasUltimateFeatureOfInterest"] = field
				new_row["sosa:phenomenonTime"] = "".join((year, season))
				new_row["sosa:hasResult"] = row["DENSITY_CLASS"] # TODO: very ugly, find better way to parse
				new_row["sosa:resultTime"] = row["DATE"]
				new_row["sosa:madeBySensor"] = row["OPERATOR"]
				new_row["unit"] = config_variables.loc["ABONDANCE", "Unit"]
				new_row["datatype"] = config_variables.loc["DENSITY_CLASS", "DataType"]

				new_row["iop:Entity"] = row["WEED_SPECIES"]
				new_row["iop:Property"] = "Density"
				new_row["iop:Constraint"] = row["PHENOLOGY_STAGE"]

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")
		

class DPUseCaseBioagressorsGeneralConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		# columns = [col for col in list(self.table.columns) if col not in ["DATE", "OPERATOR"]]

		counter = 1

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			field, _, year, season, plot = index.split("-")

			for col in ["PEST_DENSITY", "GENERAL_STATE"]:
				if not pd.isna(self.table.loc[index, col]):
					new_row = {k:None for k in COLUMN_NAMES}
					new_row["sosa:Observation"] = f"""Obs-fieldState-{field}-{"".join((year, season))}-{counter}"""
					new_row["sosa:observedProperty"] = col
					new_row["sosa:hasFeatureOfInterest"] = "-".join((field, plot))
					new_row["sosa:hasUltimateFeatureOfInterest"] = field
					new_row["sosa:phenomenonTime"] = "".join((year, season))
					new_row["sosa:hasResult"] = self.table.loc[index, col] # TODO: very ugly, find better way to parse
					new_row["sosa:resultTime"] = row["DATE"]
					new_row["sosa:madeBySensor"] =row["OPERATOR"]
					new_row["unit"] = config_variables.loc[col, "Unit"]
					new_row["datatype"] = config_variables.loc[col, "DataType"]

					out_table.loc[len(out_table)] = new_row
					counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")

class DPUseCaseBioagressorsDetailsConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, sampling:str, outfile:str):

		values = {"FieldSampled", "LabSampled"}
		if sampling not in values:
			raise ValueError("'sampling' must be one of %r" % values)

		
		columns = [col for col in list(self.table.columns) if col not in ["PLANT", "DATE", "OPERATOR"]]

		colum_names_with_constraints = COLUMN_NAMES + ["iop:Entity", "iop:Property", "iop:Constraint"]
		out_table = pd.DataFrame(columns=colum_names_with_constraints)

		counter = 1

		for index, row in tqdm(self.table.iterrows(), total=self.table.shape[0]):

			field, _, year, season, plot, plant = index.split("-")

			for col in columns:
				# print(index, col, self.table.loc[index, col])
				try:
					if not pd.isna(self.table.loc[index, col]):
						new_row = {k:None for k in colum_names_with_constraints}
						new_row["sosa:Observation"] = f"""Obs-BioAgr-{sampling}-{field}-{plot}-{plant}-{"".join((year, season))}-{counter}"""
						new_row["sosa:observedProperty"] = f"""Presence-{config_variables.loc[col, "InDbName"]}-on-{sampling}-plants"""
						new_row["sosa:hasFeatureOfInterest"] = "-".join((field, plot))
						new_row["sosa:hasUltimateFeatureOfInterest"] = field
						new_row["sosa:phenomenonTime"] = "".join((year, season))
						new_row["sosa:hasResult"] = self.table.loc[index, col] # TODO: very ugly, find better way to parse
						new_row["sosa:resultTime"] = "" # FIX ? Missing in this table because indicated in the general table ...
						if "OPERATOR" in self.table.columns:
							new_row["sosa:madeBySensor"] = row["OPERATOR"] # ?? Not in all tables
						new_row["unit"] = config_variables.loc[col, "Unit"]
						new_row["datatype"] = config_variables.loc[col, "DataType"]

						new_row["iop:Entity"] = col
						new_row["iop:Property"] = "SpeciesPresence"
						new_row["iop:Constraint"] = sampling

						out_table.loc[len(out_table)] = new_row
						counter += 1
				except ValueError as e:
					print(f"the index {index} is duplicated somewhere : all data of all involved rows will be ignored")
					#print(index, col, self.table.loc[index, col])

		out_table.to_csv(outfile, index=False, sep="\t")

class DPUseCaseBioagressorsLabConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		colum_names_with_constraints = COLUMN_NAMES + ["iop:Entity", "iop:Property", "iop:Constraint"]
		out_table = pd.DataFrame(columns=colum_names_with_constraints)

		self.table.set_index(["DATE", "OPERATOR"], inplace=True, append=True)
		self.table = self.table.stack(future_stack=True)

		print(self.table.head())

		counter = 1

		for index, val in tqdm(self.table.items(), total=self.table.shape[0]):

			if not pd.isna(val):

				ident = index[0].split("-")
				
				new_row = {k:None for k in colum_names_with_constraints}
				new_row["sosa:Observation"] = f"""Obs-BioAgr-LabSampled-{ident[0]}-{ident[4]}-{ident[5]}-{ident[2]}-{ident[3]}-{counter}"""
				new_row["sosa:observedProperty"] = f"""Presence-{config_variables.loc[index[3], "InDbName"]}-on-LabSampled-plants"""
				new_row["sosa:hasFeatureOfInterest"] = "-".join((ident[0], ident[4]))
				new_row["sosa:hasUltimateFeatureOfInterest"] = ident[0]
				new_row["sosa:phenomenonTime"] = "".join((ident[2], ident[3]))
				
				if val == 0.0:
					new_row["sosa:hasResult"] = 0
				elif val == 1.0:
					new_row["sosa:hasResult"] = 1
				else:
					new_row["sosa:hasResult"] = val

				new_row["sosa:resultTime"] = index[1]
				new_row["sosa:madeBySensor"] = ident[2] # Warning : not in FieldSampled tables
				new_row["unit"] = config_variables.loc[index[3], "Unit"]
				new_row["datatype"] = config_variables.loc[index[3], "DataType"]

				new_row["iop:Entity"] = config_variables.loc[index[3], "InDbName"]
				new_row["iop:Property"] = "SpeciesPresence"
				new_row["iop:Constraint"] = "LabSampled"

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile, index=False, sep="\t")


class DPUseCaseClimaticConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		out_table = pd.DataFrame(columns=COLUMN_NAMES)

		cols = ["year", "month", "day_of_month"]
		self.table["DATE"] = self.table[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
		self.table.drop(["day_of_year","day_of_month", "month", "year"], axis=1, inplace=True)
		self.table.set_index(['DATE'], inplace=True, append=True)
		self.table = self.table.stack(future_stack=True)

		for idx, val in tqdm(self.table.items(), total=self.table.shape[0]):
			new_row = {k:None for k in COLUMN_NAMES}
			new_row["sosa:Observation"] = f"""Obs-Climatic-{idx[0]}-{idx[1]}-{idx[2]}"""
			new_row["sosa:observedProperty"] = idx[2]
			new_row["sosa:hasFeatureOfInterest"] = idx[0]
			new_row["sosa:hasUltimateFeatureOfInterest"] = np.nan
			new_row["sosa:phenomenonTime"] = np.nan
			new_row["sosa:hasResult"] = val
			new_row["sosa:resultTime"] = idx[1]
			new_row["sosa:madeBySensor"] = np.nan
			new_row["unit"] = config_variables.loc[idx[2], "Unit"]
			new_row["datatype"] = config_variables.loc[idx[2], "DataType"]

			out_table.loc[len(out_table)] = new_row

		out_table.to_csv(outfile, index=False, sep="\t")


class DPUseCaseFeatureOfInterestConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, outfile:str):		

		out_table = pd.DataFrame(columns=["Name", "InDbName", "InDbType", "AltURI", "thing:locatedIn"])

		# Regions
		regions = self.table["REGION".unique()]
		regions = {k:k[0]+k[1:].lower() for k in regions}

		for k, v in regions.keys():
			new_row = {k:"" for k in out_table.columns}

			new_row["Name"] = k
			new_row["InDbName"] = v
			new_row["InDbType"] = "Region"
			new_row["AltURI"] = "thing:Place"

			out_table.loc[len(out_table)] = new_row

		# SAFRAN
		safran = self.table["SAFRAN".unique()]
		safran = {k:"" for k in safran}

		for _, row in self.table.iterrows():

			if safran[row["SAFRAN"]] == "":
				new_row = {k:"" for k in out_table.columns}

				new_row["Name"] = row["SAFRAN"]
				new_row["InDbName"] = f"""MailleSafran-{row["SAFRAN"]}"""
				new_row["InDbType"] = "SampledField"
				new_row["AltURI"] = "thing:Place"
				new_row["thing:locatedIn"] = row["REGION"]

				out_table.loc[len(out_table)] = new_row
		
		# Sampled fields
		for index, row in self.table.iterrows():
			new_row = {k:"" for k in out_table.columns}

			# Sampling Fields
			new_row["Name"] = index
			new_row["InDbName"] = index.split()[0]
			new_row["InDbType"] = "SampledField"
			new_row["AltURI"] = "thing:Place,envo:00000114"
			new_row["thing:locatedIn"] = regions[row["REGION"]]

			out_table.loc[len(out_table)] = new_row

		# Sampling plots
		plots = ("PA", "PB", "PC", "PD", "P1", "P2", "P3", "P4")

		for index, row in self.table.iterrows():
			
			for plot in plots:
				new_row = {k:"" for k in out_table.columns}

				new_row["Name"] = f"{index}-{plot}"
				new_row["InDbName"] = f"{index.split()[0]}-{plot}"
				new_row["InDbType"] = "SamplingPlot"
				new_row["AltURI"] = "thing:Place,agro:00000301"
				new_row["thing:locatedIn"] = f"{index.split()[0]}"

				out_table.loc[len(out_table)] = new_row

		out_table.to_csv(outfile, sep="\t")		
