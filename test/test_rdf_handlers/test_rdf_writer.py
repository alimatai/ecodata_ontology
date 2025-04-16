#!/usr/bin/env python

from genecodata.rdf_handlers.triples_classes import TurtleTriple, TurtleTripleSet
from genecodata.rdf_handlers.rdf_writer import TurtleWriter

PREFIXDICT = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
	"thing": "https://schema.org/Thing",
	"envo": "http://purl.obolibrary.org/obo/envo.owl",
	"sosa": "http://www.w3.org/ns/sosa/"
}

TRIPLESET = TurtleTripleSet([
	TurtleTriple("dp:AF001", "rdf:type", "thing:Place"),
	TurtleTriple("dp:AF001", "rdf:type", "envo:00000114"),
	TurtleTriple("dp:AF001", "rdf:type", "sosa:FeatureOfInterest")
])

def test_writes_prefixes():

	expected_content = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	"""

	turtle_writer = TurtleWriter(PREFIXDICT, "output_test_writes_prefixes.ttl")
	turtle_writer.write_prefixes()

	with open("output_test_writes_prefixes.ttl", "r") as f:
		output = f.read()

	assert output == expected_content

def test_write_tripleset():
	
	expected_content = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dp:SampledField rdf:type sosa:FeatureOfInterest .
dp:SampledField rdf:type thing:Place .
dp:SampledField rdf:type envo:00000114 .
dp:SamplingPlot rdf:type sosa:FeatureOfInterest .
dp:SamplingPlot rdf:type thing:Place .
dp:SamplingPlot rdf:type agro:00000301 .
	"""

	turtle_writer = TurtleWriter(PREFIXDICT, "output_test_writes_prefixes.ttl")
	turtle_writer.write_prefixes()
	turtle_writer.write_tripleset(TRIPLESET)

	with open("output_test_writes_prefixes.ttl", "r") as f:
		output = f.read()

	assert output == expected_content

if __name__ == "__main__":
	test_writes_prefixes()
	test_write_tripleset()
