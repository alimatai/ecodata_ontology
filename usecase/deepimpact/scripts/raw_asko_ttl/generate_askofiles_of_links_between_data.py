#!/usr/bin/env python

import os
import argparse
import pandas as pd

"""
Creates the askofiles building the links between askofiles made from raw data (and already concatenated) of DeepImpact. These files are actually listings of:
- Sensors
- Temporalities
- Dates
- Safran cells
- Sampled Fields
- Sampling Plots in Fields
- Sampled Plants in Plots
- Constraints (i-adopt)

(Basically everything which is not a sosa:Property)
"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-dir", help="Directory with all data" )
parser.add_argument("-o", "--output-dir", help="Output directory")
args=parser.parse_args()

# Temporalities 
# -------------
# (WARNING : hard-coded here because it is small; if too big : parse all tables and get unique values)

df = pd.DataFrame({"Temporality": ["Y1", "Y2", "Y1S1", "Y1S2", "YS1", "Y2S2"],
				   "includedIn@Temporality": ["","", "Y1", "Y1", "Y2", "Y2"]})

df.to_csv(os.path.join(args.output_dir, "temporalities.tsv"), sep="\t", index=False)

# Sensors 
# -------
# (WARNING : hard-coded here because it is small; if too big : parse all tables and get unique values)
# Question : How to handle multiple values with Askofiles ? (in RDF, make a bag, but in askofiles ??)

sensors = ["CG,FR","CG,OB","CG,OB,RZ","CG,RD","CG,RZ","CM,LL","CM,LLB","EC,TD,LL,CM","FR,CG","FR,CG,OB","FR,RD,RZ","FR,RZ","FV","FV,OB","FV,RZ","KG,LLB,CM","KGN","LL","LL,CM","LL,CM,TD,EC","LLB,CHM,KGN","MC","OB","OB,CG","PLG","PLG,CM,LL","PLG,JC","PLG,SC","PLG,UK,SD","RD,CG","RZ,BM,CG","RZ,RD","RZ,RD,FR","SC","SC,KG","SC,KG,OB,EC","SD,UK,PLG","TD,EC","UK,EV","UK,SC,EC,EV"]
sensorstypes = ["Person"]*len(sensors)

df = pd.DataFrame({"Sensor": sensors, "Type":sensorstypes})
df.to_csv(os.path.join(args.output_dir, "sensors.tsv"), sep="\t", index=False)

# Features On Interest : sampled fields
# -------------------------------------

df = pd.read_csv(os.path.join(args.input_dir, "location.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t",
	decimal=",")

df["SAFRAN"] = df["SAFRAN"].apply(lambda x: "SafranCell-{}".format(str(x)))
df.rename({"FIELD_ID": "SampledField", "SAFRAN": "locatedIn@SafranCell"}, axis=1, inplace=True)
df.drop(["LATITUDE", "LONGITUDE"], axis=1, inplace=True)
df.to_csv(os.path.join(args.output_dir, "sampled_fields.tsv"), sep="\t", index=False)

# Features Of interest : safran grid cells
# ----------------------------------------
# Messy but working

safran_id = df["locatedIn@SafranCell"].unique()
safran_nb = [snb.replace("SafranCell-", "") for snb in safran_id]
safran = pd.DataFrame({"SafranCell": safran_id, "CellID": safran_nb})

safran.to_csv(os.path.join(args.output_dir, "safran_cells.csv"), sep="\t", index=False)

# Sampling Plots
# --------------
# (Could also be done with itertools.product)

possible_plots = ('-PA', '-PB', '-PC', '-PD', '-P1', '-P2', '-P3', '-P4')
plots = [field + plot for field in df["SampledField"] for plot in possible_plots]

fields = [field[0:11] for field in plots]

df = pd.DataFrame({
    "SamplingPlot": plots, 
    "locatedIn@SampledField": fields})

df.to_csv(os.path.join(args.output_dir, "sampling_plots.tsv"), sep="\t", index=False)

# Sampled Plants
# --------------

df = pd.read_csv(os.path.join(args.input_dir, "bioagressors_field_details.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t",
	decimal=",")

sampled_plants = list(df["SAMPLED_PLANT"].apply(lambda x: f"""{x}-FieldSampled"""))
# sampling_plots = list(df["SAMPLED_PLANT"].apply(lambda x: "-".join(x.split("-")[0:-1])))
sampling_plots = list(df["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[4]}"""))
constraint = ["FieldSampled"] * len(df.index)

df = pd.read_csv(os.path.join(args.input_dir, "bioagressors_lab.tsv"), 
	index_col=None, 
	header=0, 
	sep="\t",
	decimal=",")

# Ugly but it works
sampled_plants += list(df["SAMPLED_PLANT"].apply(lambda x: f"""{x}-LabSampled"""))
# sampling_plots += list(df["SAMPLED_PLANT"].apply(lambda x: "-".join(x.split("-")[0:-1])))
# sampling_plots += list(df["SAMPLED_PLANT"].apply(lambda x: "-".join([x.split("-")[0], x.split("-")[1], x.split("-")[2], x.split("-")[4]])))
sampling_plots += list(df["SAMPLED_PLANT"].apply(lambda x: f"""{x.split("-")[0]}-{x.split("-")[1]}-{x.split("-")[2]}-{x.split("-")[4]}"""))
constraint += ["LabSampled"] * len(df.index)

df = pd.DataFrame({"SampledPlant": sampled_plants, "sampleOf@SamplingPlot":sampling_plots, "constrainedBy@Constraint":constraint})

df.to_csv(os.path.join(args.output_dir, "sampled_plants.tsv"), sep="\t", index=False)

# Entities
# --------
# (weeds and bioagressors species)

# Constraints
# -----------

df = pd.DataFrame({
	"Constraint":["FieldSampled", "LabSampled", "PhenologyStage-A", "PhenologyStage-B", "PhenologyStage-C", "PhenologyStage-D", "PhenologyStage-E"],
	"ConstraintLabel":["FieldSampledPlant", "LabSampledPlant", "PlantInPhenologyStage-A", "PlantInPhenologyStage-B", "PlantInPhenologyStage-C", "PlantInPhenologyStage-D", "PlantInPhenologyStage-E"]
})

df.to_csv(os.path.join(args.output_dir, "constraints.tsv"), sep="\t", index=False)

# Dates