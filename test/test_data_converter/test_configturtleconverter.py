#!/usr/bin/env python

from genecodata.data_converter.data_converter import ConfigTurtleConverter
from genecodata.rdf_handlers.triples_classes import RDFTriple
import pandas as pd

TRIPLE = RDFTriple("dp:AF001", "rdf:type", "thing:Place")

data_test = pd.DataFrame.from_dict({
	"Name" : ["BiomassWeed", "FineSand", "SampledField", "SamplingPlot"],
	"MainUri" : ["sosa:ObservableProperty", "sosa:ObservableProperty", "sosa:FeatureOfInterest", "sosa:FeatureOfInterest"],
	"altURI" : ["to:0000352", "envo:06105273", "thing:Place,envo:00000114", "thing:Place,agro:00000301"],
	"Set" : ["Biomass", "SoilBiochemistry", "nan", "nan"]
})

converter_test = ConfigTurtleConverter("dp", data_test)

def test_features_of_interest_triples():
	
	expected_data = [
		RDFTriple("dp:SampledField", "rdf:type", "FeatureOfInterest"),
		RDFTriple("dp:SampledField", "rdf:type", "thing:Place"),
		RDFTriple("dp:SampledField", "rdf:type", "envo:00000114"),
		RDFTriple("dp:SamplingPlot", "rdf:type", "sosa:FeatureOfInterest"),
		RDFTriple("dp:SamplingPlot", "rdf:type", "thing:Place"),
		RDFTriple("dp:SamplingPlot", "rdf:type", "agro:00000301"),]

	assert converter_test.features_of_interest_triples == expected_data

def test_observable_properties_triples():

	expected_data = [
		RDFTriple("dp:BiomassWeed", "rdf:type", "sosa:ObservableProperty"),
		RDFTriple("dp:BiomassWeed", "rdf:type", "to:0000352"),
		RDFTriple("dp:FineSand", "rdf:type", "sosa:ObservableProperty"),
		RDFTriple("dp:FineSand", "rdf:type", "envo:06105273"),
		RDFTriple("dp:Biomass", "iop:hasMember", "dp:BiomassWeed"),
		RDFTriple("dp:FineSand", "iop:hasMember", "dp:SoilBiochemistry"),]

	assert converter_test.observable_properties_triples == expected_data

def test_variablesets_triples():

	expected_data = [
		RDFTriple("dp:Biomass", "rdf:type", "iop:VariableSet"),
		RDFTriple("dp:SoilBiochemistry", "rdf:type", "iop:VariableSet"),
	]

	assert converter_test.variablesets_triples() == expected_data

if __name__ == "__main__":
	test_features_of_interest_triples()
	test_observable_properties_triples()
	test_variablesets_triples()