#!/usr/bin/env python

from genecodata.rdf_handlers.triples_classes import RDFTriple, RDFTriplesSet

TRIPLE = RDFTriple("dp:AF001", "rdf:type", "thing:Place")

# TODO add NaN
TRIPLESET = RDFTriplesSet([
	RDFTriple("dp:AF001", "rdf:type", "thing:Place"),
	RDFTriple("dp:AF001", "rdf:type", "envo:00000114"),
	RDFTriple("dp:AF001", "rdf:type", "sosa:FeatureOfInterest")
])

def test_turtletriplesub():
	assert TRIPLE.sub == "dp:AF001"

def test_turtletriplepred():
	assert TRIPLE.pred == "rdf:type"

def test_turtletripleobj():
	assert TRIPLE.obj == "thing:Place"

def test_turtletriplesetsub():
	assert TRIPLESET.sub == "dp:AF001"

def test_turtletriplesetpairs():
	assert TRIPLESET.pred_obj_pairs == [
		("rdf:type","thing:Place"),
		("rdf:type","envo:00000114"),
		("rdf:type","sosa:FeatureOfInterest")
	]

def test_writeturtletriplesset():
	TRIPLESET.write("test_write.ttl", "w")

if __name__ == "__main__":
    test_turtletriplesub()
    test_turtletriplepred()
    test_turtletripleobj()
    test_turtletriplesetsub()
    test_turtletriplesetpairs()