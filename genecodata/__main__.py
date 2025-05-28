#!/usr/bin/env python

from genecodata.data_converter.data_converter import GraphManager, TemporalityConverter, SensorConverter, ObservablePropertiesConverter, ConstraintConverter, ObservationConverter, FeatureOfInterestConverter, SampleConverter

#import genecodata.data_converter as gdc

import pandas as pd
import argparse
import os
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--obs-dir", help="directory with all required tab-separated files of sosa:Observations" )
parser.add_argument("-c", "--config-dir", help="Directory with all config files of sosa:Property/iop:Variable, sosa:FeatureOfInterest, sosa:Temporalities ...")
parser.add_argument("-p", "--instances-prefix", help="prefix that will used to the project instances")
parser.add_argument("-o", "--output-rdf", help="output RDF file") # TODO : make several files named with a common prefix/suffix
args=parser.parse_args()

# genecodata -i usecase/deepimpact/data/genecodata_input_data/ -c usecase/deepimpact/config/ -p di -o usecase/deepimpact/data/output_data/rdf/graph.ttl

# -------------------------------------- #
# Build the graph with the package classes
# -------------------------------------- #

# with open(args.prefixes, 'r') as f:
# 	PREFIXES = json.load(f)

def main():

	# Graph
	# -----

	graph = GraphManager(json.load(open(os.path.join(args.config_dir, "config_prefixes.json"), "r")))
	graph.bind_prefixes()

	# Configuration
	# -------------

	start = time.time()
	
	df = TemporalityConverter(pd.read_csv(os.path.join(args.config_dir, "config_temporalities.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))
	
	print("Temporalities triples...") # TODO use decorators later
	df.build_triples(graph)

	df = SensorConverter(pd.read_csv(os.path.join(args.config_dir, "config_sensors.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))
	
	print("Sensors triples...") # TODO use decorators later
	df.build_triples(graph)
	
	df = ObservablePropertiesConverter(pd.read_csv(os.path.join(args.config_dir, "config_variables.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))
	
	print("Observable Properties triples...") # TODO use decorators later
	df.build_variables_triples(graph)
	print("Variables sets triples...") # TODO use decorators later
	df.build_variables_sets_triples(graph)

	df = ConstraintConverter(pd.read_csv(os.path.join(args.config_dir, "config_constraints.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))		

	df.build_triples(graph)

	df = FeatureOfInterestConverter(pd.read_csv(os.path.join(args.config_dir, "config_features_of_interest.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))		

	print("Features Of Interest triples...")
	df.build_triples(graph)

	df = SampleConverter(pd.read_csv(os.path.join(args.config_dir, "config_samples.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))		

	print("Samples triples...")
	df.build_triples(graph)

	end = time.time()

	print(f"""Configuration triples built in {end - start} seconds""")

	# Observations
	# ------------

	# TODO fix dates format before main script
	# TODO : do a loop on the observations folder instead

	start = time.time()

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_biomasses.tsv"),
			header=0,
			index_col=0,
			sep="\t"))

	print("Biomasses observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_yields.tsv"),
			header=0,
			index_col=0,
			sep="\t"))	
	df.table["sosa:resultTime"] = df.table["sosa:resultTime"].str.strip(" 00:00:00") # tofix in classes

	print("Yields observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_nirs.tsv"),
			header=0,
			index_col=0,
			sep="\t"))

	print("NIRS observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_agriculture.tsv"),
			header=0,
			index_col=0,
			sep="\t"))

	print("Agriculture practices observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_soils_biochemistry.tsv"),
			header=0,
			index_col=0,
			sep="\t"))

	print("Soils biochemistry observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_weeds.tsv"),
			header=0,
			index_col=0,
			sep="\t"))
	df.table["sosa:resultTime"] = df.table["sosa:resultTime"].str.strip(" 00:00:00") # tofix in classes

	print("Weeds observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_bioagressors_field_general.tsv"),
			header=0,
			index_col=0,
			sep="\t"))
	df.table["sosa:resultTime"] = df.table["sosa:resultTime"].str.strip(" 00:00:00") # tofix in classes

	print("Bioagressors field (1) observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_bioagressors_field_details.tsv"),
			header=0,
			index_col=0,
			sep="\t"))
	df.table["sosa:resultTime"] = df.table["sosa:resultTime"].str.strip(" 00:00:00")

	# Fix all types before, in usecase classes - (very bullying !)
	df.table["sosa:hasResult"] = df.table["sosa:hasResult"].astype(float) # tofix in classes
	df.table["sosa:hasResult"] = df.table["sosa:hasResult"].astype(int) # tofix in classes

	print("Bioagressors field (2) observations triples...")
	df.build_triples(graph)

	types = {
		"sosa:observedProperty": str,
		"sosa:hasFeatureOfInterest": str,
		"sosa:hasUltimateFeatureOfInterest": str,
		"sosa:hasResult": str,
		"sosa:resultTime": str,
		"sosa:phenomenonTime": str,
		"sosa:madeBySensor": str,
		"unit": str,
		"datatype": str,
		"iop:Entity": str,
		"iop:Property": str,
		"iop:Constraint": str
	}

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_bioagressors_lab.tsv"),
			header=0,
			index_col=0,
			sep="\t",
			dtype = types))
	df.table["sosa:resultTime"] = df.table["sosa:resultTime"].fillna("").str.strip(" 00:00:00") # tofix in classes
	df.table["sosa:hasResult"] = df.table["sosa:hasResult"].str.strip(".0") # tofix in classes

	print("Bioagressors lab observations triples...")
	df.build_triples(graph)

	df = ObservationConverter(
		pd.read_csv(os.path.join(args.obs_dir, "observations_climatic.tsv"),
			header=0,
			index_col=0,
			sep="\t"))

	# df.table["sosa:hasFeatureOfInterest"] = df.table["sosa:hasFeatureOfInterest"].apply(str)

	print("Climatic observations triples...")
	df.build_triples(graph)

	end = time.time()

	print(f"""Observation triples built in {end - start} seconds""")
	
	print("Saving graph...")
	start = time.time()
	graph.g.serialize(destination=args.output_rdf ,format="turtle")
	end = time.time()
	print(f"""Graph saved in {end - start} seconds""")	

if __name__ == '__main__':
	main()