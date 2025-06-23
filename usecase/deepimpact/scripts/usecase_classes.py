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
					
					if not pd.isna(config_variables.loc[col, "InDbName"]):
						new_row["sosa:observedProperty"] = config_variables.loc[col, "InDbName"]
					else:
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
					
					if not pd.isna(config_variables.loc[col, "InDbName"]):
						new_row["sosa:observedProperty"] = config_variables.loc[col, "InDbName"]
					else:
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
					
					if not pd.isna(config_variables.loc[col, "InDbName"]):
						new_row["sosa:observedProperty"] = config_variables.loc[col, "InDbName"]
					else:
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
					
					if not pd.isna(config_variables.loc[col, "InDbName"]):
						new_row["sosa:observedProperty"] = config_variables.loc[col, "InDbName"]
					else:
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
		colum_names_with_constraints = COLUMN_NAMES + ["iop:hasObjectOfInterest", "iop:hasProperty", "iop:hasConstraint"]
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

				new_row["iop:hasObjectOfInterest"] = row["WEED_SPECIES"]
				new_row["iop:hasProperty"] = "Density"
				new_row["iop:hasConstraint"] = row["PHENOLOGY_STAGE"]

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
										
					if not pd.isna(config_variables.loc[col, "InDbName"]):
						new_row["sosa:observedProperty"] = config_variables.loc[col, "InDbName"]
					else:
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

class DPUseCaseBioagressorsFieldConverter():

	def __init__(self, general_table:pd.DataFrame, detail_table:pd.DataFrame):
		self.general_table = general_table
		self.detail_table = detail_table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		colum_names_with_constraints = COLUMN_NAMES + ["iop:hasObjectOfInterest", "iop:hasProperty", "iop:hasConstraint"]
		out_table = pd.DataFrame(columns=colum_names_with_constraints)

		self.detail_table = self.detail_table.stack(future_stack=True)

		counter = 1

		for index, val in tqdm(self.detail_table.items(), total=self.detail_table.shape[0]):

			variable = index[1]

			if not pd.isna(val):

				ident = index[0].split("-")
				
				new_row = {k:None for k in colum_names_with_constraints}
				new_row["sosa:Observation"] = f"""Obs-BioAgr-FieldSampled-{ident[0]}-{ident[4]}-{ident[5]}-{ident[2]}-{ident[3]}-{counter}"""
									
				if not pd.isna(config_variables.loc[variable, "InDbName"]):
					new_row["sosa:observedProperty"] = f"""{config_variables.loc[variable, "InDbName"]}-on-FieldSampled-plants"""
				else:
					new_row["sosa:observedProperty"] = f"""{variable}-on-FieldSampled-plants"""
				
				new_row["sosa:hasFeatureOfInterest"] = f"""{ident[0]}-{ident[4]}-{ident[5]}-Field"""
				new_row["sosa:hasUltimateFeatureOfInterest"] = "-".join((ident[0], ident[4]))
				new_row["sosa:phenomenonTime"] = "".join((ident[2], ident[3]))
				
				if val == 0.0:
					new_row["sosa:hasResult"] = 0
				elif val == 1.0:
					new_row["sosa:hasResult"] = 1
				else:
					new_row["sosa:hasResult"] = val

				new_row["sosa:resultTime"] = self.general_table.loc["-".join(ident[0:5]),"DATE"]
				new_row["sosa:madeBySensor"] = self.general_table.loc["-".join(ident[0:5]),"OPERATOR"]
				new_row["unit"] = config_variables.loc[variable, "Unit"]
				new_row["datatype"] = config_variables.loc[variable, "DataType"]

				new_row["iop:hasObjectOfInterest"] = config_variables.loc[variable, "InDbName"]

				if config_variables.loc[variable, "Set"] == "BioagressorPresence":
					new_row["iop:hasProperty"] = "SpeciesPresence"
				elif config_variables.loc[variable, "Set"] == "PlantPhenotype":
					new_row["iop:hasProperty"] = "Phenotype"
				else :
					new_row["iop:hasProperty"] = "Undefined"

				new_row["iop:hasConstraint"] = "FieldSampled"

				out_table.loc[len(out_table)] = new_row
				counter += 1

		out_table.to_csv(outfile, float_format='%.0f', index=False, sep="\t")

class DPUseCaseBioagressorsLabConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):

		colum_names_with_constraints = COLUMN_NAMES + ["iop:hasObjectOfInterest", "iop:hasProperty", "iop:hasConstraint"]
		out_table = pd.DataFrame(columns=colum_names_with_constraints)

		self.table.set_index(["DATE", "OPERATOR"], inplace=True, append=True)
		self.table = self.table.stack(future_stack=True)

		counter = 1

		for index, val in tqdm(self.table.items(), total=self.table.shape[0]):

			if not pd.isna(val):

				ident = index[0].split("-")
				
				new_row = {k:None for k in colum_names_with_constraints}
				new_row["sosa:Observation"] = f"""Obs-BioAgr-LabSampled-{ident[0]}-{ident[4]}-{ident[5]}-{ident[2]}-{ident[3]}-{counter}"""

				if not pd.isna(config_variables.loc[index[3], "InDbName"]):
					new_row["sosa:observedProperty"] = f"""{config_variables.loc[index[3], "InDbName"]}-on-LabSampled-plants"""
				else:
					new_row["sosa:observedProperty"] = f"""{index[3]}-on-LabSampled-plants"""
				
				new_row["sosa:hasFeatureOfInterest"] = f"""{ident[0]}-{ident[4]}-{ident[5]}-Lab"""
				new_row["sosa:hasUltimateFeatureOfInterest"] = "-".join((ident[0], ident[4]))
				new_row["sosa:phenomenonTime"] = "".join((ident[2], ident[3]))
				
				# Veeeery dirty (fix later when more free-time, likely in the concatenation script run before)
				if val == 0.0:
					new_row["sosa:hasResult"] = 0
				elif val == 1.0:
					new_row["sosa:hasResult"] = 1
				else:
					new_row["sosa:hasResult"] = val

				new_row["sosa:resultTime"] = index[1]
				new_row["sosa:madeBySensor"] = index[2]
				new_row["unit"] = config_variables.loc[index[3], "Unit"]
				new_row["datatype"] = config_variables.loc[index[3], "DataType"]

				new_row["iop:hasObjectOfInterest"] = config_variables.loc[index[3], "InDbName"]

				if config_variables.loc[index[3], "Set"] == "BioagressorPresence":
					new_row["iop:hasProperty"] = "SpeciesPresence"
				elif config_variables.loc[index[3], "Set"] == "PlantPhenotype":
					new_row["iop:hasProperty"] = "Phenotype"
				else :
					new_row["iop:hasProperty"] = "Undefined"

				new_row["iop:hasConstraint"] = "LabSampled"
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
			new_row["sosa:Observation"] = f"""Obs-Climatic-Safran-{idx[0]}-{idx[1]}-{idx[2]}"""
			
			if not pd.isna(config_variables.loc[idx[2], "InDbName"]):
				new_row["sosa:observedProperty"] = config_variables.loc[idx[2], "InDbName"]
			else:
				new_row["sosa:observedProperty"] = idx[2]

			new_row["sosa:hasFeatureOfInterest"] = f"""Safran-{idx[0]}"""
			new_row["sosa:hasUltimateFeatureOfInterest"] = np.nan
			new_row["sosa:phenomenonTime"] = np.nan
			new_row["sosa:hasResult"] = val
			new_row["sosa:resultTime"] = idx[1]
			new_row["sosa:madeBySensor"] = np.nan
			new_row["unit"] = config_variables.loc[idx[2], "Unit"]
			new_row["datatype"] = config_variables.loc[idx[2], "DataType"]

			out_table.loc[len(out_table)] = new_row

		out_table.to_csv(outfile, index=False, sep="\t")


class DPUseCaseAgriculturalPracticesConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, config_variables:pd.DataFrame, outfile:str):		

		out_table = pd.DataFrame(columns=COLUMN_NAMES)
		
		# We do not integrate verything, just a few
		test_columns = ["OPERATOR","CROP","AGRI_TYPE","CONVENTIONAL_ORGANIC","PRODUCTION_POTENTIAL","SOIL_DEPTH","LIVESTOCK","NAME_CROP_Y","MAIN_CROP_Y","NB_COMPANION_PLANT_Y","COMPANION_PLANT_Y","NB_COVER_CROPPING_Y","NAME_COVER_CROPPING_Y"]

		self.table = self.table[test_columns]
		self.table.set_index(["OPERATOR"], inplace=True, append=True)
		self.table = self.table.stack(future_stack=True)
		self.table.dropna(inplace=True)

		counter = 1
		for index, val in tqdm(self.table.items(), total=self.table.shape[0]):

			ident = index[0].split("-")

			new_row = {k:None for k in COLUMN_NAMES}
			new_row["sosa:Observation"] = f"""Obs-AgriParctice-{ident[0]}-{counter}"""

			if not pd.isna(config_variables.loc[index[2], "InDbName"]):
				new_row["sosa:observedProperty"] = config_variables.loc[index[2], "InDbName"]
			else:
				new_row["sosa:observedProperty"] = index[2]

			new_row["sosa:hasFeatureOfInterest"] = ident[0]
			new_row["sosa:hasUltimateFeatureOfInterest"] = np.nan
			new_row["sosa:phenomenonTime"] = ident[2]
			new_row["sosa:hasResult"] = val
			new_row["sosa:resultTime"] = np.nan
			new_row["sosa:madeBySensor"] = index[1]
			new_row["unit"] = config_variables.loc[index[2], "Unit"]
			new_row["datatype"] = "xsd:string"

			out_table.loc[len(out_table)] = new_row
			counter +=1

		out_table.to_csv(outfile, index=False, sep="\t")


class DPUseCaseFeatureOfInterestConverter():

	def __init__(self, table:pd.DataFrame):
		self.table = table

	def convert(self, outfile:str):		

		out_table = pd.DataFrame(columns=["Name", "InDbName", "InDbType", "AltURI", "thing:locatedIn"])

		# Regions
		regions = self.table["REGION"].unique()
		regions = {k:k[0]+k[1:].lower() for k in regions}

		for k,v in regions.items():
			new_row = {k:"" for k in out_table.columns}

			new_row["Name"] = k
			new_row["InDbName"] = v
			new_row["InDbType"] = "Region"
			new_row["AltURI"] = "thing:Place"

			out_table.loc[len(out_table)] = new_row

		# SAFRAN
		safran = self.table["SAFRAN"].unique()
		safran = {k:"" for k in safran}

		for _, row in self.table.iterrows():

			if safran[row["SAFRAN"]] == "":
				new_row = {k:"" for k in out_table.columns}

				new_row["Name"] = row["SAFRAN"]
				new_row["InDbName"] = f"""Safran-{row["SAFRAN"]}"""
				new_row["InDbType"] = "SampledField"
				new_row["AltURI"] = "thing:Place"
				new_row["thing:locatedIn"] = regions[row["REGION"]]

				out_table.loc[len(out_table)] = new_row
		
		# Sampled fields
		for index, row in self.table.iterrows():
			new_row = {k:"" for k in out_table.columns}

			# Sampling Fields
			new_row["Name"] = index
			new_row["InDbName"] = index.split()[0]
			new_row["InDbType"] = "SampledField"
			new_row["AltURI"] = "thing:Place,obo:ENVO_00000114"
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
				new_row["AltURI"] = "thing:Place,obo:AGRO_00000301"
				new_row["thing:locatedIn"] = f"{index.split()[0]}"

				out_table.loc[len(out_table)] = new_row

		out_table.to_csv(outfile, sep="\t", index=False)	

class DPUseCaseSampleConverter():
		
	def __init__(self, tablefield:pd.DataFrame, tablelab:pd.DataFrame):
		self.tablefield = tablefield
		self.tablelab = tablelab

	def convert(self, outfile:str):

		out_table = pd.DataFrame(columns=["Name", "InDbName", "InDbType", "AltURI", "sosa:isSampleOf"])

		print("Field samples ...")
		for idx in tqdm(self.tablefield.index, total=self.tablefield.shape[0]):

			ident = idx.split("-")

			new_row = {k:"" for k in out_table.columns}
			new_row["Name"] = f"""{ident[0]}-{ident[4]}-{ident[5]}-field"""
			new_row["InDbName"] = f"""{ident[0]}-{ident[4]}-{ident[5]}-field"""
			new_row["InDbType"] = "SampledPlant"
			new_row["AltURI"] = "obo:PO_0000003"
			new_row["sosa:isSampleOf"] = f"""{ident[0]}-{ident[4]}"""

			out_table.loc[len(out_table)] = new_row

		print("Lab samples ...")
		for idx in tqdm(self.tablelab.index, total=self.tablelab.shape[0]):

			ident = idx.split("-")

			new_row = {k:"" for k in out_table.columns}
			new_row["Name"] = f"""{ident[0]}-{ident[4]}-{ident[5]}-lab"""
			new_row["InDbName"] = f"""{ident[0]}-{ident[4]}-{ident[5]}-lab"""
			new_row["InDbType"] = "SampledPlant"
			new_row["AltURI"] = "obo:PO_0000003"
			new_row["sosa:isSampleOf"] = f"""{ident[0]}-{ident[4]}"""

			out_table.loc[len(out_table)] = new_row
		
		out_table.to_csv(outfile, sep="\t", index=False)	