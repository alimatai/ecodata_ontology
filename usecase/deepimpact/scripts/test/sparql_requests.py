#!/usr/bin/env python

from rdflib import Graph
import argparse
from linetimer import CodeTimer

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graph", help="graph to request" )
args=parser.parse_args()

g = Graph()
g.parse(args.graph)

# Queries
# -------

# Returns all sosa:ObservableProperties
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX sosa: <http://www.w3.org/ns/sosa/>

	SELECT ?obsprop
	WHERE {
		?obsprop rdf:type sosa:Property .
	}
"""

with CodeTimer('Request : all sosa:Property', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["obsprop"])

# Returns all variables sets
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX iop: <https://w3id.org/iadopt/ont/>
	
	SELECT ?varset
	WHERE {
		?varset rdf:type iop:VariableSet .
	}
"""

with CodeTimer('Request : all iop:VariableSet', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["varset"])

# Returns all couples of variable / variableSet
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX sosa: <http://www.w3.org/ns/sosa/>
	PREFIX iop: <https://w3id.org/iadopt/ont/>
	
	SELECT ?obsprop ?varset
	WHERE {
		?varset iop:hasMember ?obsprop .
	}
	ORDER BY ?varset
"""

with CodeTimer('Request : all sosa:Property in iop:Variable = SoilBiochemistry', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["obsprop"], r["varset"])


# Returns all sosa:ObservableProperties which are in the category VariableSet:SoilBiochemistry
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX sosa: <http://www.w3.org/ns/sosa/>
	PREFIX iop: <https://w3id.org/iadopt/ont/>
	PREFIX di: <file:///home/vmataign/Documents/genecodata/usecase/deepimpact/data/output_data/rdf/>
	
	SELECT ?obsprop
	WHERE {
		?obsprop a sosa:Property .
		di:SoilBiochemistry iop:hasMember ?obsprop .
	}
"""

with CodeTimer('Request : all sosa:Property in iop:Variable = SoilBiochemistry', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["obsprop"])

# Returns all fields
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX obo: <http://purl.obolibrary.org/obo/>

	SELECT ?field
	WHERE {
		?field rdf:type obo:ENVO_00000114 . 
	}
"""

with CodeTimer('Request : all sampled fields', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["field"])


# Returns all fields located in the region `West`
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX obo: <http://purl.obolibrary.org/obo/>
	PREFIX thing: <https://schema.org/>
	PREFIX di: <file:///home/vmataign/Documents/genecodata/usecase/deepimpact/data/output_data/rdf/>

	SELECT ?field ?region
	WHERE {
		?field rdf:type obo:ENVO_00000114 . 
		?field thing:locatedIn ?region .
  	VALUES ( ?region ) {(di:West)}
	}
"""

"""
Or:
SELECT ?field
	WHERE {
		?field rdf:type obo:ENVO_00000114 . 
		?field thing:locatedIn di:West .
	}
"""

with CodeTimer('Request : all fields in region West', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["field"])

# Returns the full SoilBiochemistry data for fields in the region `South` sampled in year 1, season 2
q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX sosa: <http://www.w3.org/ns/sosa/>
	PREFIX iop: <https://w3id.org/iadopt/ont/>
	PREFIX di: <file:///home/vmataign/Documents/genecodata/usecase/deepimpact/data/output_data/rdf/>
	
	SELECT ?obsprop ?value ?field
	WHERE {
		?obsprop_ rdf:type sosa:Property .
		?observation_ sosa:observedProperty ?obsprop_ .
  		di:SoilBiochemistry iop:hasMember ?obsprop_ .
  		?observation_ sosa:hasFeatureOfInterest ?field_ .
  		?observation_ sosa:hasSimpleResult ?value .
  		?observation_ sosa:phenomenonTime di:Y1S2 .

  		BIND (REPLACE(str(?obsprop_), "^.*/([^/]*)$", "$1") AS ?obsprop) .
  		BIND (REPLACE(str(?field_), "^.*/([^/]*)$", "$1") AS ?field) .
	}
"""

with CodeTimer('Request : SoilBiochemistry data for fields in teh region South, year 1 season 2', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["value"])

# Returns yields of B. napus fields of year 2, alongside farming type, organic matter in soil

q = """
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX sosa: <http://www.w3.org/ns/sosa/>
	PREFIX iop: <https://w3id.org/iadopt/ont/>
	PREFIX di: <file:///home/vmataign/Documents/genecodata/usecase/deepimpact/data/output_data/rdf/>
"""

with CodeTimer('Request : SoilBiochemistry data for fields in teh region South, year 1 season 2', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["value"])