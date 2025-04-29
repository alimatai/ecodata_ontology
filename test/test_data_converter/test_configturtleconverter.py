#!/usr/bin/env python

from genecodata.data_converter.data_converter import PrefixesBinder, ObservablePropertiesConverter, ConstraintConverter
# from genecodata.rdf_handlers.triples_classes import RDFTriple
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
import pandas as pd

# TRIPLE = RDFTriple("dp:AF001", "rdf:type", "thing:Place")

data_test = pd.DataFrame.from_dict({
	"Name" : ["BiomassWeed", "FineSand", "WeightTotal", "preliq_q"],
	"MainUri" : ["sosa:ObservableProperty", "sosa:ObservableProperty", "sosa:ObservableProperty", "sosa:ObservableProperty"],
	"altURI" : ["to:0000352", "envo:06105273", "", ""],
	"Set" : ["Biomass", "SoilBiochemistry", "Yields", "Climatic"]
})

observable_properties = ObservablePropertiesConverter(data_test)

def test_observable_properties_triples():

	expected_data = Graph()
	expected_data.add((URIRef("BiomassWeed"), RDF.type, URIRef("sosa:ObservableProperty")))
	expected_data.add((URIRef("BiomassWeed"), RDF.type, URIRef("to:0000352")))
	expected_data.add((URIRef("Biomass"), URIRef("iop:hasMember"), URIRef("BiomassWeed")))
	expected_data.add((URIRef("FineSand"), RDF.type, URIRef("sosa:ObservableProperty")))
	expected_data.add((URIRef("FineSand"), RDF.type, URIRef("envo:06105273")))
	expected_data.add((URIRef("SoilBiochemistry"), URIRef("iop:hasMember"), URIRef("FineSand")))
	expected_data.add((URIRef("WeightTotal"), RDF.type, URIRef("sosa:ObservableProperty")))
	expected_data.add((URIRef("Yields"), URIRef("iop:hasMember"), URIRef("WeightTotal")))
	expected_data.add((URIRef("preliq_q"), RDF.type, URIRef("sosa:ObservableProperty")))
	expected_data.add((URIRef("Climatic"), URIRef("iop:hasMember"), URIRef("preliq_q")))
	
	assert observable_properties.observable_properties_triples() == expected_data

def test_variablesets_triples():

	expected_data = Graph()
	expected_data.add((URIRef("Biomass"), RDF.type, URIRef("iop:VariableSet")))
	expected_data.add((URIRef("SoilBiochemistry"), RDF.type, URIRef("iop:VariableSet")))
	expected_data.add((URIRef("Yields"), RDF.type, URIRef("iop:VariableSet")))
	expected_data.add((URIRef("Climatic"), RDF.type, URIRef("iop:VariableSet")))

	assert observable_properties.variablesets_triples() == expected_data


data_test = pd.DataFrame.from_dict({
	"Name" : ["RO", "RS", "LF", "PHENOLOGY_STAGE"],
	"InDbName" : ["Root", "Rhizopshere", "Leaf", "PhenologyStage"],
	"ConstraintOf" : ["Abundance", "Abundance", "Abundance", "Abundance"],
	"AltURI" : ["po:0009005", "envo:00005801", "po:0025034", "po:0007033"],
	"DataType" : ["", "", "", "xsd:string"]
})

constraints = ConstraintConverter(data_test)

def test_constraints_triples():

	expected_data= Graph()
	expected_data.add((URIRef("Root"), RDF.type, URIRef("iop:Constraint")))
	expected_data.add((URIRef("Root"), RDF.type, URIRef("po:0009005")))
	expected_data.add((URIRef("Rhizopshere"), RDF.type, URIRef("iop:Constraint")))
	expected_data.add((URIRef("Rhizopshere"), RDF.type, URIRef("envo:00005801")))
	expected_data.add((URIRef("Leaf"), RDF.type, URIRef("iop:Constraint")))
	expected_data.add((URIRef("Leaf"), RDF.type, URIRef("po:0025034")))
	expected_data.add((URIRef("PhenologyStage"), RDF.type, URIRef("iop:Constraint")))
	expected_data.add((URIRef("PhenologyStage"), RDF.type, URIRef("po:0007033")))

	assert constraints.constraints_triples() == expected_data

if __name__ == "__main__":
	test_observable_properties_triples()
	test_variablesets_triples()
	test_constraints_triples()