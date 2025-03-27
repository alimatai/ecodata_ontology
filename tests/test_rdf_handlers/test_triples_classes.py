#!/usr/bin/env python

from genecodata_integration.src.triples_classes import TurtleTriple, TurtleTripleSet

def test_turtletriplesub():
	triple = TurtleTriple("dp:AF001", "rdf:type", "thing:Place") 
	assert triple.getsubject == "dp:AF001"

def test_turtletriplepred():
	triple = TurtleTriple("dp:AF001", "rdf:type", "thing:Place") 
	assert triple.getpredicate == "rdf:type"

def test_turtletripleobj():
	triple = TurtleTriple("dp:AF001", "rdf:type", "thing:Place") 
	assert triple.getobject == "thing:Place"

def test_turtletriplesetsub():

	triples = [
		TurtleTriple("dp:AF001", "rdf:type", "thing:Place"),
		TurtleTriple("dp:AF001", "rdf:type", "envo:00000114"),
		TurtleTriple("dp:AF001", "rdf:type", "sosa:FeatureOfInterest")
	]

	tripleset = TurtleTripleSet(triples)

	assert tripleset.subject == "dp:AF0001"

def test_turtletriplesetpairs():

	triples = [
		TurtleTriple("dp:AF001", "rdf:type", "thing:Place"),
		TurtleTriple("dp:AF001", "rdf:type", "envo:00000114"),
		TurtleTriple("dp:AF001", "rdf:type", "sosa:FeatureOfInterest")
	]

	tripleset = TurtleTripleSet(triples)

	assert tripleset.pred_obj_pairs == [("rdf:type","thing:Place"),("rdf:type","envo:00000114"),("rdf:type","sosa:FeatureOfInterest")]

if __name__ == "__main__":
    test_turtletriplesub()
    test_turtletriplepred()
    test_turtletripleobj()
    test_turtletriplesetsub()
    test_turtletriplesetpairs()
