#!/usr/bin/env python

from genecodata.data_converter.data_converter import *
import pandas as pd

import argparse
import os

"""
This program converts DeepImpact data to templates suited for the conversion into a genecodata RDF graph

Inputs : 

- Directory with all config files

1) 
"""

from usecase_classes import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-data", help="format-friendly DeepImpact tabular data")
parser.add_argument("-c", "--config-folder", help="directory containing all the tsv config files")
parser.add_argument("-o", "--output-dir", help="output directory for genecodata ready files")
args=parser.parse_args()

# -i : /home/vmataign/Documents/genecodata/usecase/deepimpact/data/concatenated_input_data
# -c : /home/vmataign/Documents/genecodata/usecase/deepimpact/config
# -o : /home/vmataign/Documents/genecodata/usecase/deepimpact/data/genecodata_input_data

# ------------------------------------- #
# Get data (concatenated from raw data) #
# ------------------------------------- #

agriculture = pd.read_csv(os.path.join(args.input_data, "agriculture.tsv"), header=0, index_col=0, sep="\t")
biomasses = pd.read_csv(os.path.join(args.input_data, "biomass.tsv"), header=0, index_col=0, sep="\t")
yields = pd.read_csv(os.path.join(args.input_data, "yields.tsv"), header=0, index_col=0, sep="\t")
nirs = pd.read_csv(os.path.join(args.input_data, "nirs.tsv"), header=0, index_col=0, sep="\t")
soils = pd.read_csv(os.path.join(args.input_data, "soils.tsv"), header=0, index_col=0, sep="\t")
weeds = pd.read_csv(os.path.join(args.input_data, "weeds.tsv"), header=0, index_col=0, sep="\t")
bioagressors_lab_df = pd.read_csv(os.path.join(args.input_data, "bioagressors_lab.tsv"), header=0, index_col=0, sep="\t")
bioagressors_field_details_df = pd.read_csv(os.path.join(args.input_data, "bioagressors_field_details.tsv"), header=0, index_col=0, sep="\t")
bioagressors_field_general = pd.read_csv(os.path.join(args.input_data, "bioagressors_field_general.tsv"), header=0, index_col=0, sep="\t")
climatic = pd.read_csv(os.path.join(args.input_data, "climatic.tsv"), header=0, index_col=0, sep="\t")
features_of_interest = pd.read_csv(os.path.join(args.input_data, "location.tsv"), header=0, index_col=0, sep="\t")

# ----------------------------------------------------------- #
# Convert data to graph input format with the UseCase classes #
# ----------------------------------------------------------- #

config_variables = pd.read_csv(os.path.join(args.config_folder, "config_variables.tsv"), header=0, index_col=0, sep="\t")

agriculture = DPUseCaseAgriculturalPracticesCOnverter(agriculture)
biomasses = DPUseCaseBiomassConverter(biomasses)
yields = DPUseCaseYieldsConverter(yields)
nirs = DPUseCaseNirsConverter(nirs)
soils = DPUseCaseSoiBiochemistryConverter(soils)
weeds = DPUseCaseWeedsConverter(weeds)
bioagressors_field_details = DPUseCaseBioagressorsFieldConverter(bioagressors_field_general, bioagressors_field_details_df)
bioagressors_field_general = DPUseCaseBioagressorsGeneralConverter(bioagressors_field_general)
bioagressors_lab = DPUseCaseBioagressorsLabConverter(bioagressors_lab_df)
climatic = DPUseCaseClimaticConverter(climatic)

features_of_interest = DPUseCaseFeatureOfInterestConverter(features_of_interest)
samples = DPUseCaseSampleConverter(bioagressors_lab_df, bioagressors_field_details_df)

print("agriculture...")
agriculture.convert(config_variables, os.path.join(args.output_dir, "observations_agriculture.tsv"))
print("biomasses...")
biomasses.convert(config_variables, os.path.join(args.output_dir, "observations_biomasses.tsv"))
print("yields...")
yields.convert(config_variables, os.path.join(args.output_dir, "observations_yields.tsv"))
print("nirs...")
nirs.convert(config_variables, os.path.join(args.output_dir, "observations_nirs.tsv"))
print("soils...")
soils.convert(config_variables, os.path.join(args.output_dir, "observations_soils_biochemistry.tsv"))
print("weeds...")
weeds.convert(config_variables, os.path.join(args.output_dir, "observations_weeds.tsv"))
print("bioagressors field general...")
bioagressors_field_general.convert(config_variables, os.path.join(args.output_dir, "observations_bioagressors_field_general.tsv"))
print("bioagressors field details...")
bioagressors_field_details.convert(config_variables, os.path.join(args.output_dir, "observations_bioagressors_field_details.tsv"))
print("bioagressors lab...")
bioagressors_lab.convert(config_variables, os.path.join(args.output_dir, "observations_bioagressors_lab.tsv"))
print("climatic...")
climatic.convert(config_variables, os.path.join(args.output_dir, "observations_climatic.tsv"))
print("features of interest...")
features_of_interest.convert(os.path.join(args.config_folder, "config_features_of_interest.tsv"))
print("samples...")
samples.convert(os.path.join(args.config_folder, "config_samples.tsv"))