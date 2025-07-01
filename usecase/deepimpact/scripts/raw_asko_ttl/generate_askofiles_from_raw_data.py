#!/usr/bin/env python

import os
import argparse
import pandas as pd

"""
Converts DeepImpact raw (and already concatenated) data to generalist askofiles able to be converted later to the sosa + iadopt schema

In summary, for each loaded data table :
- Columns names are rewritten with compatible askomics headers
- Some columns are modified to match lined entities names (for example for matching plots and sampled plants, IDs have to be slightly modified)
- Some askomics columns are added : @Temporality, @Sensors, @Date ...
"""

# Ugly code to fix (done quickly to have a working prototype to show):
# TODO 1) : many copy warnings when using pd.apply()
# TODO 2) : hardly readable code lines in the bioagressors part
# TODO 3) pandas columns typing : ".0" are added to numerical data. 
# 	-> Fixed in a really ugly way by parsing columns and replace ".0" by "".
#	-> redo that properly (with dtypes when reading files ?)

# ISSUE : how to declare iop:Entities for the formalisation of variables in I-Adopt ?

# -> An iop:Entity is a part of a iop:Variable which can have the property the iop:ObjectOfInterest, 
# on which is bound a iop:Constraint. in DeepImpact, iop:Entities are WeedSpecies and
# Bioagressors species (respectively constrained by the phenological stage and the 
# sampling method (lab / field))

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-dir", help="Directory with all data" )
parser.add_argument("-o", "--output-dir", help="Output directory")
args=parser.parse_args()


# Agricultural practices
# ----------------------

df = pd.read_csv(os.path.join(args.input_dir, "agriculture.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["FIELD_ID"].apply(lambda x: x.split("-")[2])
df["AgriculturalPractice"] = ["AgriPracticeData-{}".format(i) for i in range(1, len(df.index)+1)]
df.rename({"FIELD_ID": "FeatureOfInterest@SampledField", "OPERATOR": "madeBySensor@Sensor"}, axis=1, inplace=True)
df.set_index(df["AgriculturalPractice"], inplace=True, drop=True)
df.drop(["REGION", "AgriculturalPractice"], axis=1, inplace=True)

for col in df.columns:
	df[col] = df[col].apply(lambda x: str(x).replace(".0", ""))
df = df.replace("nan", '', regex=True)

df = df.reindex(sorted(df.columns), axis=1)

df.to_csv(os.path.join(args.output_dir, "agriculture.tsv"), sep="\t")

# Bioagressors
# ------------
# lab and field

dflab = pd.read_csv(os.path.join(args.input_dir, "bioagressors_lab.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

dffielddet = pd.read_csv(os.path.join(args.input_dir, "bioagressors_field_details.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

# Very weird encoding at some points (AF019-Y1-S1-PA at least). Add a fix in contanation scripts ?
dffielddet["SAMPLED_PLANT"] = dffielddet["SAMPLED_PLANT"].apply(lambda x: str(x).replace(u'\xa0', u''))

dffieldgen = pd.read_csv(os.path.join(args.input_dir, "bioagressors_field_general.tsv"), 
	index_col=0, # index is needed for that one 
	header=0, 
	sep="\t", 
	decimal=",")

# Columns sets

common_lab_cols = ["SAMPLED_PLANT", 
	"DATE",
	"OPERATOR"]

pheno_cols_lab = [
	"PLANT_DEVELOPMENT_STAGE",
	"NUMBER_OF_LIVING_LEAVES",
	"NUMBER_OF_STEMS",
	"PLANT_HEIGHT",
	"OVERALL_FOLIAR_PARASITISM",
	"OVERALL_FOLIAR_PHYTOPHAGY",
	"N_SPOTS_PARASITIC_FUNGI",
	"ROOT_DAMAGES",
	"NUMBER_OF_THALLUS_PER_PLANT",
	"MAIN_THALLUS_HEIGHT"]

pheno_cols_field = ["OVERALL_FOLIAR_PARASITISM", "OVERALL_FOLIAR_PHYTOPHAGY", "NUMBER_OF_THALLUS_PER_PLANT"]

# Bioagressors lab

dfbl = dflab.loc[:,~dflab.columns.isin(pheno_cols_lab)]

dfbl["phenomenonTime@Temporality"] = dfbl["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
dfbl["hasUltimateFeatureOfInterest@SampledField"] = dfbl["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}""")
dfbl["SAMPLED_PLANT"] = dfbl["SAMPLED_PLANT"].apply(lambda x: f"""{x}-LabSampled""")
dfbl["Bioagressor"] = ["Bioagressor-{}".format(i) for i in range(1, len(dfbl.index)+1)]
dfbl.rename({"SAMPLED_PLANT": "FeatureOfInterest@SampledPlant", "DATE": "resultTime@Date", "OPERATOR": "madeBySensor@Sensor"}, axis=1, inplace=True)
dfbl.set_index(dfbl["Bioagressor"], inplace=True, drop=True)
dfbl.drop(["Bioagressor"], axis=1, inplace=True)
dfbl["constrainedBy@Constraint"] = ["LabSampled"] * len(dfbl.index)

# Bioagressors field

dfbf = dffielddet.loc[:,~dffielddet.columns.isin(pheno_cols_field)]
dfbf["phenomenonTime@Temporality"] = dfbf["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
dfbf["hasUltimateFeatureOfInterest@SampledField"] = dfbf["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}""")
dfbf["Bioagressor"] = ["Bioagressor-{}".format(i) for i in range(1, len(dfbf.index)+1)]
dfbf["resultTime@Date"] = dfbf["SAMPLED_PLANT"].apply(lambda x: dffieldgen.loc[f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[3]}-{x.split("-")[4]}""", "DATE"])
dfbf["madeBySensor@Sensor"] = dfbf["SAMPLED_PLANT"].apply(lambda x: dffieldgen.loc[f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[3]}-{x.split("-")[4]}""", "OPERATOR"])
dfbf["SAMPLED_PLANT"] = dfbf["SAMPLED_PLANT"].apply(lambda x: f"""{x}-FieldSampled""")
dfbf.rename({"SAMPLED_PLANT": "FeatureOfInterest@SampledPlant"}, axis=1, inplace=True)
dfbf.set_index(dfbf["Bioagressor"], inplace=True, drop=True)
dfbf.drop(["Bioagressor"], axis=1, inplace=True)
dfbf["constrainedBy@Constraint"] = ["FieldSampled"] * len(dfbf.index)

dff = pd.concat([dfbl, dfbf])

for col in dff.columns:
	dff[col] = dff[col].apply(lambda x: str(x).replace(".0", ""))
dff = dff.replace("nan", '', regex=True)

dff.to_csv(os.path.join(args.output_dir, "bioagressors.tsv"), sep="\t")

# Plant Phenotype
# ---------------
# in lab sampled + 2 cols of field sampled

dfppl = dflab[common_lab_cols+pheno_cols_lab]

dfppl["phenomenonTime@Temporality"] = dfppl["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
dfppl["hasUltimateFeatureOfInterest@SampledField"] = dfppl["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}""")
dfppl["SampledPlantPhenotype"] = ["LabSampledPlantPhenotype-{}".format(i) for i in range(1, len(dfppl.index)+1)]
dfppl["SAMPLED_PLANT"] = dfppl["SAMPLED_PLANT"].apply(lambda x: f"""{x}-LabSampled""")
dfppl.rename({"SAMPLED_PLANT": "FeatureOfInterest@SampledPlant", "DATE": "resultTime@Date", "OPERATOR": "madeBySensor@Sensor"}, axis=1, inplace=True)
dfppl.set_index(dfppl["SampledPlantPhenotype"], inplace=True, drop=True)
dfppl.drop(["SampledPlantPhenotype"], axis=1, inplace=True)
dfppl["constrainedBy@Constraint"] = ["LabSampled"] * len(dfppl.index)


dfppf = dffielddet[["SAMPLED_PLANT", "OVERALL_FOLIAR_PARASITISM", "OVERALL_FOLIAR_PHYTOPHAGY", "NUMBER_OF_THALLUS_PER_PLANT"]]

dfppf["phenomenonTime@Temporality"] = dfppf["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
dfppf["hasUltimateFeatureOfInterest@SampledField"] = dfppf["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}""")
dfppf["SampledPlantPhenotype"] = ["FieldSampledPlantPhenotype-{}".format(i) for i in range(1, len(dfppf.index)+1)]
dfppf["resultTime@Date"] = dfppf["SAMPLED_PLANT"].apply(lambda x: dffieldgen.loc[f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[3]}-{x.split("-")[4]}""", "DATE"])
dfppf["madeBySensor@Sensor"] = dfppf["SAMPLED_PLANT"].apply(lambda x: dffieldgen.loc[f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[3]}-{x.split("-")[4]}""", "OPERATOR"])
dfppf["SAMPLED_PLANT"] = dfppf["SAMPLED_PLANT"].apply(lambda x: f"""{x}-FieldSampled""")
dfppf.rename({"SAMPLED_PLANT": "FeatureOfInterest@SampledPlant"}, axis=1, inplace=True)
dfppf.set_index(dfppf["SampledPlantPhenotype"], inplace=True, drop=True)
dfppf.drop(["SampledPlantPhenotype"], axis=1, inplace=True)
dfppf["constrainedBy@Constraint"] = ["FieldSampled"] * len(dfppf.index)

# Merge and write
dff = pd.concat([dfppl, dfppf])

for col in ["NUMBER_OF_LIVING_LEAVES","NUMBER_OF_STEMS","PLANT_HEIGHT","N_SPOTS_PARASITIC_FUNGI","ROOT_DAMAGES","NUMBER_OF_THALLUS_PER_PLANT","MAIN_THALLUS_HEIGHT"]:
	dff[col] = dff[col].apply(lambda x: str(x).replace(".0", ""))
dff = dff.replace("nan", '', regex=True)

dff.to_csv(os.path.join(args.output_dir, "plant_phenotype.tsv"), sep="\t")

# Field Health State
# ------------------

df = pd.read_csv(os.path.join(args.input_dir, "bioagressors_field_general.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["PLOT_ID_SEASONAL"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
df["FieldHealthState"] = ["FieldHealthState-{}".format(i) for i in range(1, len(df.index)+1)]
df["PLOT_ID_SEASONAL"] = df["PLOT_ID_SEASONAL"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[4]}""")
df.rename({"PLOT_ID_SEASONAL": "FeatureOfInterest@SamplingPlot", "DATE": "resultTime@Date", "OPERATOR": "madeBySensor@Sensor"}, axis=1, inplace=True)
df.set_index(df["FieldHealthState"], inplace=True, drop=True)
df.drop(["FieldHealthState"], axis=1, inplace=True)

for col in ["NB_ONE_METER","MORE_ONE_METER"]:
	df[col] = df[col].apply(lambda x: str(x).replace(".0", ""))
df = df.replace("nan", '', regex=True)

df.to_csv(os.path.join(args.output_dir, "field_health_state.tsv"), sep="\t")

# Biomasses
# ---------

df = pd.read_csv(os.path.join(args.input_dir, "biomass.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["PLOT_ID_ANNUAL"].apply(lambda x: x.split("-")[2])
df["BiomassData"] = ["BiomassData-{}".format(i) for i in range(1, len(df.index)+1)]
df.rename({"PLOT_ID_ANNUAL": "FeatureOfInterest@SamplingPlot", "OPERATOR": "madeBySensor@Sensor", "DATE": "resultTime@Date"}, axis=1, inplace=True)
df.set_index(df["BiomassData"], inplace=True, drop=True)
df.drop(["BiomassData"], axis=1, inplace=True)

for col in ["ROW_NUMBER", "PLANT_DENSITY"]:
	df[col] = df[col].apply(lambda x: str(x).replace(".0", ""))
df = df.replace("nan", '', regex=True)

df.to_csv(os.path.join(args.output_dir, "biomass.tsv"), sep="\t")

# Climatic
# ---------

df = pd.read_csv(os.path.join(args.input_dir, "climatic.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

# Add leading 0 for correct date format
df["month"] = df["month"].astype(str).apply('{:0>2}'.format)
df["day_of_month"] = df["day_of_month"].astype(str).apply('{:0>2}'.format)

df["resultTime@Date"] = df[["year", "month","day_of_month", ]].apply(lambda x: '-'.join(x.values.astype(str)), axis=1)
df.drop(["day_of_year","day_of_month", "month", "year"], axis=1, inplace=True)

df["ClimaticData"] = ["ClimaticData-{}".format(i) for i in range(1, len(df.index)+1)]
df["SAFRAN"] = df["SAFRAN"].apply(lambda x: "SafranCell-{}".format(str(x)))
df.rename({"SAFRAN": "FeatureOfInterest@SafranCell"}, axis=1, inplace=True)
df.set_index(df["ClimaticData"], inplace=True, drop=True)
df.drop(["ClimaticData"], axis=1, inplace=True)

df.to_csv(os.path.join(args.output_dir, "climatic.tsv"), sep="\t")

# Dates
# -----
# (All dates of the project are included in climatic data)
dates = df["resultTime@Date"].unique()
df = pd.DataFrame({"Date": ["Date-{}".format(i) for i in range(1, len(dates)+1)], "DateValue": dates})
df.to_csv(os.path.join(args.output_dir, "dates.tsv"), sep="\t", index=False)


# Nirs
# ----

df = pd.read_csv(os.path.join(args.input_dir, "nirs.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["PLOT_ID_ANNUAL"].apply(lambda x: x.split("-")[2])
df["NirsData"] = ["NirsData-{}".format(i) for i in range(1, len(df.index)+1)]
df.rename({"PLOT_ID_ANNUAL": "FeatureOfInterest@SamplingPlot", "OPERATOR": "madeBySensor@Sensor", "DATE": "resultTime@Date"}, axis=1, inplace=True)
df.set_index(df["NirsData"], inplace=True, drop=True)
df.drop(["NirsData"], axis=1, inplace=True)

df.to_csv(os.path.join(args.output_dir, "nirs.tsv"), sep="\t")

# Soils Biochem
# -------------

df = pd.read_csv(os.path.join(args.input_dir, "soils.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["FIELD_SUB_ID"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
df["SoilBiochemData"] = ["SoilBiochemData-{}".format(i) for i in range(1, len(df.index)+1)]
df["FIELD_SUB_ID"] = df["FIELD_SUB_ID"].apply(lambda x: x[:-3])
df.rename({"FIELD_SUB_ID": "FeatureOfInterest@SampledField"}, axis=1, inplace=True)
df.set_index(df["SoilBiochemData"], inplace=True, drop=True)
df.drop(["SoilBiochemData"], axis=1, inplace=True)

for col in ["COARSE_SAND","FINE_SAND","COARSE_SILT","FINE_SILT","CLAY", "CEC"]:
	df[col] = df[col].apply(lambda x: str(x).replace(".0", ""))
df = df.replace("nan", '', regex=True)

df.to_csv(os.path.join(args.output_dir, "soils.tsv"), sep="\t")

# Weeds
# -----

df = pd.read_csv(os.path.join(args.input_dir, "weeds.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["PLOT_ID_SEASONAL"].apply(lambda x: f"""{x.split("-")[2]}{x.split("-")[3]}""")
df["WeedsData"] = ["WeedsData-{}".format(i) for i in range(1, len(df.index)+1)]
df["PHENOLOGY_STAGE"] = df["PHENOLOGY_STAGE"].apply(lambda x:f"""PhenologyStage-{x}""" if not pd.isna(x) else "")
df["PLOT_ID_SEASONAL"] = df["PLOT_ID_SEASONAL"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[4]}""")
df.rename({"PLOT_ID_SEASONAL": "FeatureOfInterest@SamplingPlot", 
	"OPERATOR": "madeBySensor@Sensor", 
	"DATE": "resultTime@Date",
	"WEED_SPECIES": "ObjectOfInterest@Entity", # Declared as a iop:Entity
	"PHENOLOGY_STAGE": "constrainedBy@Constraint"}, axis=1, inplace=True)
df.set_index(df["WeedsData"], inplace=True, drop=True)
df.drop(["WeedsData", "ABONDANCE"], axis=1, inplace=True)

df.to_csv(os.path.join(args.output_dir, "weeds.tsv"), sep="\t")

# Yields
# ------

df = pd.read_csv(os.path.join(args.input_dir, "yields.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df["phenomenonTime@Temporality"] = df["PLOT_ID_ANNUAL"].apply(lambda x: x.split("-")[2])
df["YieldData"] = ["YieldData-{}".format(i) for i in range(1, len(df.index)+1)]
df.rename({"PLOT_ID_ANNUAL": "FeatureOfInterest@SamplingPlot", "OPERATOR": "madeBySensor@Sensor", "DATE": "resultTime@Date"}, axis=1, inplace=True)
df.set_index(df["YieldData"], inplace=True, drop=True)
df.drop(["YieldData", "DATE_FRESH_SEEDS", "DATE_DRY_SEEDS"], axis=1, inplace=True)

for col in ["NB_RANKS","NB_UNITS"]:
	df[col] = df[col].apply(lambda x: str(x).replace(".0", ""))
df = df.replace("nan", '', regex=True)

df.to_csv(os.path.join(args.output_dir, "yields.tsv"), sep="\t")

# Entities
# --------

df = pd.read_csv(os.path.join(args.input_dir, "weeds.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t", 
	decimal=",")

df = pd.DataFrame({"Entity": df["WEED_SPECIES"].unique(), "EntityLabel": df["WEED_SPECIES"].unique()})

# Missing : bioagressors species

df.to_csv(os.path.join(args.output_dir, "entities.tsv"), sep="\t", index=False)
