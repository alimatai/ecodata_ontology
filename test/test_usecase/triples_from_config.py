#!/usr/bin/env python

from genecodata.rdf_handlers.triples_classes import RDFTriple
from genecodata.data_converter.data_converter import ObservablePropertiesConverter, PrefixesBinder
from genecodata.data_parser.tabular_data_parsers import TxtParser
from genecodata.rdf_handlers.rdf_writer import TurtleWriter

from rdflib import Graph, URIRef
import pandas as pd

import argparse
import os

"""
Inputs : directory with all config files

1) 
"""

from test.test_usecase import usecase_classes

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config-input-folder", help="directory containing all the tsv config files")
parser.add_argument("-o", "--output-rdf", help="output RDF file") # TODO : make several files named with a common prefix/suffix
args=parser.parse_args()

temporalities = usecase_classes.DPUseCaseTemporalityConverter(pd.read_csv(os.path.join(args.config_input_folder, "config_temporalities.tsv"), header=0, index_col=0, sep="\t"))
sensors = usecase_classes.DPUseCaseSensorConverter(pd.read_csv(os.path.join(args.config_input_folder, "config_sensors.tsv"), header=0, index_col=0, sep="\t"))
features_of_interest = usecase_classes.DPUseCaseFeatureOfInterestCategorizer(pd.read_csv(os.path.join(args.config_input_folder, "config_features_of_interest.tsv"), header=0, index_col=0, sep="\t"))
observable_properties = ObservablePropertiesConverter(pd.read_csv(os.path.join(args.config_input_folder, "config_variables.tsv"), header=0, index_col=0, sep="\t"))
prefixes = PrefixesBinder(pd.read_csv(os.path.join(args.config_input_folder, "config_prefixes.tsv"), header=0, index_col=0, sep="\t"))

g = Graph()

prefixes.bind_prefixes(g)
temporalities.temporalities_triples(g)
sensors.sensors_triples(g)
features_of_interest.region_triples(g)
features_of_interest.locations_triples(g)
observable_properties.observable_properties_triples(g)
observable_properties.variablesets_triples(g)

g.serialize()
