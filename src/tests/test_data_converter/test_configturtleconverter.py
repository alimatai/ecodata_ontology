#!/usr/bin/env python

from ...data_converter.data_converter import ConfigTurtleConverter
from ...rdf_handlers.triples_classes import TurtleTriple
import pandas as pd

TRIPLE = TurtleTriple("dp:AF001", "rdf:type", "thing:Place")

data_test = pd.DataFrame.from_dict({
	"Name" : ["BiomassWeed", "FineSand", "SampledField", "SamplingPlot"],
	"MainUri" : ["sosa:ObservableProperty", "sosa:ObservableProperty", "sosa:FeatureOfInterest", "sosa:FeatureOfInterest"],
	"altURI" : ["to:0000352", "envo:06105273", "thing:Place,envo:00000114", "thing:Place,agro:00000301"],
	"Set" : ["Biomass", "SoilBiochemistry", "na", "na"]
})

converter_test = ConfigTurtleConverter("dp", data_test)

def test_features_of_interest_triples():
	
	expected_data = [
		TurtleTriple("dp:SampledField", "rdf:type", "FeatureOfInterest"),
		TurtleTriple("dp:SampledField", "rdf:type", "thing:Place"),
		TurtleTriple("dp:SampledField", "rdf:type", "envo:00000114"),
		TurtleTriple("dp:SamplingPlot", "rdf:type", "sosa:FeatureOfInterest"),
		TurtleTriple("dp:SamplingPlot", "rdf:type", "thing:Place"),
		TurtleTriple("dp:SamplingPlot", "rdf:type", "agro:00000301"),]

	assert converter_test.features_of_interest_triples == expected_data

def test_observable_properties_triples():

	expected_data = [
		TurtleTriple("dp:BiomassWeed", "rdf:type", "sosa:ObservableProperty"),
		TurtleTriple("dp:BiomassWeed", "rdf:type", "to:0000352"),
		TurtleTriple("dp:FineSand", "rdf:type", "sosa:ObservableProperty"),
		TurtleTriple("dp:FineSand", "rdf:type", "envo:06105273"),
		TurtleTriple("dp:Biomass", "iop:hasMember", "dp:BiomassWeed"),
		TurtleTriple("dp:FineSand", "iop:hasMember", "dp:SoilBiochemistry"),]

	assert converter_test.observable_properties_triples == expected_data

def test_variablesets_triples():

	expected_data = [
		TurtleTriple("dp:Biomass", "rdf:type", "iop:VariableSet"),
		TurtleTriple("dp:SoilBiochemistry", "rdf:type", "iop:VariableSet"),
	]

if __name__ == "__main__":
	test_features_of_interest_triples()
	test_observable_properties_triples()
	test_variablesets_triples()