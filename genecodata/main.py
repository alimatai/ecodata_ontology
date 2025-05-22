#!/usr/bin/env python

from genecodata.data_converter import GraphManager, TemporalityConverter, SensorConverter, ObservablePropertiesConverter, ConstraintConverter

import pandas as pd
import argparse
import os

# PREFIXDICT = {
#     "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
#     "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
#     "xsd": "http://www.w3.org/2001/XMLSchema#",
# 	"thing": "https://schema.org/Thing",
# 	"envo": "http://purl.obolibrary.org/obo/envo.owl",
# 	"sosa": "http://www.w3.org/ns/sosa/",
#     "time": "https://www.w3.org/2006/time#",
#     "iop": "https://w3id.org/iadopt/ont/",
#     "chebi": "http://purl.obolibrary.org/obo/chebi.owl",
#     "to": "http://purl.obolibrary.org/obo/to.owl",
#     "agro": "http://purl.obolibrary.org/obo/AGRO_00000301",
#     "unit": "https://w3id.org/uom/",
#     "po": "http://purl.obolibrary.org/obo/po.owl",
#     "bago": "https://opendata.inrae.fr/bag-def",
#     "ncbitaxon": "http://purl.obolibrary.org/obo/ncbitaxon.owl"
# }

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--obs-dir", help="directory with all required tab-separated files of sosa:Observations" )
parser.add_argument("-c", "--config-dir", help="Directory with all config files of sosa:Property/iop:Variable, sosa:FeatureOfInterest, sosa:Temporalities ...")
parser.add_argument("-p", "--instances-prefix", help="prefix that will used to the project instances")
parser.add_argument("-o", "--output-rdf", help="output RDF file") # TODO : make several files named with a common prefix/suffix
args=parser.parse_args()

# -------------------------------------- #
# Build the graph with the package classes
# -------------------------------------- #

# with open(args.prefixes, 'r') as f:
# 	PREFIXES = json.load(f)

def main():

	temporalities = TemporalityConverter(pd.read_csv(os.path.join(args.input_dir, "config_temporalities.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))
	sensors = SensorConverter(pd.read_csv(os.path.join(args.input_dir, "config_sensors.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))
	observable_properties = ObservablePropertiesConverter(pd.read_csv(os.path.join(args.input_dir, "config_variables.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))
	constraints = ConstraintConverter(pd.read_csv(os.path.join(args.input_dir, "config_constraints.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))

	graph = GraphManager(pd.read_csv(os.path.join(args.input_dir, "config_prefixes.tsv"), 
		header=0, 
		index_col=0, 
		sep="\t"))

	graph.bind_prefixes()

	temporalities.build_triples(graph)
	sensors.build_triples(graph)
	observable_properties.build_variables_triples(graph)
	observable_properties.build_variables_sets_triples(graph)
	constraints.build_triples(graph)

	graph.g.serialize(destination=args.output_rdf ,format="turtle")

if __name__ == '__main__':
	main()