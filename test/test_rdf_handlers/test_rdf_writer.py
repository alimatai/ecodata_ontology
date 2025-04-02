#!/usr/bin/env python

from ...rdf_handlers.triples_classes import TurtleTriple, TurtleTripleSet
from ...rdf_handlers.rdf_writer import TurtleWriter

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

turtle_writer = TurtleWriter(PREFIXDICT, "output_test_rdf_writer.ttl")

turtle_writer.write_prefixes()
turtle_writer.write_tripleset(TRIPLESET)
