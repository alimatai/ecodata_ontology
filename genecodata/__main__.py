#!/usr/bin/env python

from genecodata.data_parser.tabular_data_parsers import TxtParser
from genecodata.data_converter.data_converter import ConfigTurtleConverter
from genecodata.rdf_handlers.rdf_writer import TurtleWriter

import argparse
import json

PREFIXDICT = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
	"thing": "https://schema.org/Thing",
	"envo": "http://purl.obolibrary.org/obo/envo.owl",
	"sosa": "http://www.w3.org/ns/sosa/",
    "time": "https://www.w3.org/2006/time#",
    "iop": "https://w3id.org/iadopt/ont/",
    "chebi": "http://purl.obolibrary.org/obo/chebi.owl",
    "to": "http://purl.obolibrary.org/obo/to.owl",
    "agro": "http://purl.obolibrary.org/obo/AGRO_00000301",
    "unit": "https://w3id.org/uom/",
    "po": "http://purl.obolibrary.org/obo/po.owl",
    "bago": "https://opendata.inrae.fr/bag-def",
    "ncbitaxon": "http://purl.obolibrary.org/obo/ncbitaxon.owl"
}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config-table", help="csv/tsv file describing the dataset")
parser.add_argument("-p", "--prefixes", help="json file listing all used prefixes and their URI")
parser.add_argument("-i", "--instances-prefix", help="prefix that will used to the project instances")
parser.add_argument("-o", "--output-rdf", help="output RDF file") # TODO : make several files named with a common prefix/suffix
args=parser.parse_args()

with open(args.prefixes, 'r') as f:
	PREFIXES = json.load(f)

def main():

	table = TxtParser(args.config_table, "\t")
	configloader = ConfigTurtleConverter(args.instances_prefix, table)

	foi = configloader.features_of_interest_triples()
	obsprops = configloader.observable_properties_triples()
	varsets = configloader.variablesets_triples()

	turtlewriter = TurtleWriter(PREFIXDICT, args.output_rdf)

	turtlewriter.write_prefixes()
	for tripleset in foi:
		turtlewriter.write_tripleset(tripleset)
	for tripleset in obsprops:
		turtlewriter.write_tripleset(tripleset)
	for tripleset in varsets:
		turtlewriter.write_tripleset(tripleset)

if __name__ == '__main__':
	main()